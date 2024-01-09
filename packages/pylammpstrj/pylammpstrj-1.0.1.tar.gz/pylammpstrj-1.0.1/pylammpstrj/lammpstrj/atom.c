#include "utils.h"

#include <ctype.h>
#include <errno.h>
#include <stddef.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <strings.h>

void atom_delete(struct Atom *atom)
{
    free(atom->additionnal_fields);
}

void atom_copy(struct Atom *dest, const struct Atom src, const struct AtomBuilder atom_builder)
{
    dest->id = src.id;
    dest->type = src.type;
    strncpy(dest->label, src.label, LABEL_LIMIT);
    memcpy(dest->position, src.position, 3 * sizeof(double));
    dest->charge = src.charge;
    dest->additionnal_fields = malloc(atom_builder.N_additional * sizeof(union AtomField));
    if (dest->additionnal_fields == NULL)
    {
        errno = ENOMEM;
        perror("Error while allocating memory (atom_copy.dest.additional_fields)");
        return;
    }
    memcpy(dest->additionnal_fields, src.additionnal_fields, atom_builder.N_additional * sizeof(union AtomField));
}

#define FIELDS_BASE_SIZE 10
#define FIELDS_SIZE_INCR 10

void get_field_names(struct AtomBuilder *ab)
{
    char buffer[READ_BUFFER_LIMIT], *ptr;
    char(*names)[FIELD_NAME_LIMIT] =
        calloc(FIELDS_BASE_SIZE, sizeof(char[FIELD_NAME_LIMIT]));

    if (names == NULL)
    {
        errno = ENOMEM;
        perror("Error while allocating memory (AtomBuilder.names)");
        return;
    }

    unsigned int names_size = FIELDS_BASE_SIZE;
    unsigned int n = 0;

    strncpy(buffer, ab->dump_format, READ_BUFFER_LIMIT);
    ptr = strtok(buffer, " ");

    while (ptr != NULL)
    {
        if (n >= names_size)
        {
            char(*new_names)[FIELD_NAME_LIMIT] =
                realloc(names, (names_size + FIELDS_SIZE_INCR) *
                                   sizeof(char[FIELD_NAME_LIMIT]));

            if (new_names == NULL)
            {
                free(new_names);
                errno = ENOMEM;
                perror("Error while reallocating memory (AtomBuilder.names)");
                return;
            }

            names_size += FIELDS_SIZE_INCR;
            names = new_names;
        }

        if (strlen(ptr) < FIELD_NAME_LIMIT - 1)  // !
            strncpy(names[n], ptr, FIELD_NAME_LIMIT);

        ptr = strtok(NULL, " ");
        n++;
    }

    ab->N_fields = n;
    names[n - 1][strcspn(names[n - 1], "\n")] = 0;
    ab->field_names = names;
}

void check_names(struct AtomBuilder *ab)
{
    ab->offsets = calloc(ab->N_fields, sizeof(size_t));
    ab->is_additional = calloc(ab->N_fields, sizeof(int));
    ab->fields_types = malloc(ab->N_fields * sizeof(enum AtomFieldType));

    if (ab->offsets == NULL || ab->is_additional == NULL ||
        ab->fields_types == NULL)
    {
        errno = ENOMEM;
        perror("Error while allocating memory (AtomBuilder.check_names)");
        return;
    }

    unsigned int N_additional = 0;
    for (unsigned int f = 0; f < ab->N_fields; f++)
    {
        (ab->fields_types)[f] = AFT_NULL;
        if (strcmp((ab->field_names)[f], "id") == 0)
        {
            (ab->offsets)[f] = offsetof(struct Atom, id);
            (ab->fields_types)[f] = AFT_INT;
        }
        else if (strcmp((ab->field_names)[f], "type") == 0)
        {
            (ab->offsets)[f] = offsetof(struct Atom, type);
            (ab->fields_types)[f] = AFT_INT;
        }
        else if (strcmp((ab->field_names)[f], "element") == 0 ||
                 strcmp((ab->field_names)[f], "label") == 0)
        {
            (ab->offsets)[f] = offsetof(struct Atom, id);
            (ab->fields_types)[f] = AFT_STRING;
        }
        else if (strlen((ab->field_names)[f]) == 1)
        {
            if ((ab->field_names)[f][0] == 'x')
                (ab->offsets)[f] = offsetof(struct Atom, position[0]);
            else if ((ab->field_names)[f][0] == 'y')
                (ab->offsets)[f] = offsetof(struct Atom, position[1]);
            else if ((ab->field_names)[f][0] == 'z')
                (ab->offsets)[f] = offsetof(struct Atom, position[2]);
            else if ((ab->field_names)[f][0] == 'q')
                (ab->offsets)[f] = offsetof(struct Atom, charge);

            if ((ab->offsets)[f] != 0) (ab->fields_types)[f] = AFT_DOUBLE;
        }
        else
        {
            (ab->offsets)[f] =
                N_additional;  // the rank in the additional_fields array
            (ab->is_additional)[f] = 1;
            N_additional++;
        }
    }
    ab->N_additional = N_additional;
}

void get_additional_types(const char line[READ_BUFFER_LIMIT],
                          struct AtomBuilder *ab)
{
    char buffer[READ_BUFFER_LIMIT];
    strncpy(buffer, line, READ_BUFFER_LIMIT);

    char *ptr = strtok(buffer, " ");

    for (unsigned int f = 0; f < ab->N_fields; ptr = strtok(NULL, " "), f++)
    {
        if (!(ab->is_additional)[f]) continue;

        if (isalpha(ptr[0]))
            (ab->fields_types)[f] = AFT_STRING;
        else
            (ab->fields_types)[f] = AFT_DOUBLE;
    }
}

static union AtomField str_to_int(const char field[READ_BUFFER_LIMIT])
{
    return (union AtomField){.i = atoi(field)};
}

static union AtomField str_to_double(const char field[READ_BUFFER_LIMIT])
{
    return (union AtomField){.d = atof(field)};
}

static union AtomField str_to_str(const char field[READ_BUFFER_LIMIT])
{
    union AtomField af;
    strncpy(af.s, field, ATOM_FIELD_STR_LIMIT);
    return af;
}

void initialize_functions(struct AtomBuilder *ab)
{
    union AtomField (**functions)(const char[READ_BUFFER_LIMIT]) =
        malloc(ab->N_fields *
               sizeof(union AtomField(*)(const char[READ_BUFFER_LIMIT])));

    if (functions == NULL)
    {
        errno = ENOMEM;
        perror("Error while allocating memory (AtomBuilder.parsing_functions)");
        return;
    }

    for (unsigned int field = 0; field < ab->N_fields; field++)
    {
        switch (ab->fields_types[field])
        {
            case AFT_INT:
                functions[field] = &str_to_int;
                break;
            case AFT_DOUBLE:
                functions[field] = &str_to_double;
                break;
            case AFT_STRING:
                functions[field] = &str_to_str;
                break;
            default:
                errno = EINVAL;
                perror("Error while scanning the types (AFT_NULL)");
                ab->parsing_functions = functions;
                return;
        }
    }
    ab->parsing_functions = functions;
}

struct AtomBuilder atom_builder_new(const char *dump_format, FILE *input)
{
    struct AtomBuilder ab;

    strncpy(ab.dump_format, dump_format, READ_BUFFER_LIMIT);

    get_field_names(&ab);
    if (errno != 0) return ab;

    check_names(&ab);
    if (errno != 0)
    {
        free(ab.field_names);
        return ab;
    }

    char line[READ_BUFFER_LIMIT];
    long pos = ftell(input);
    do
        if (fgets(line, READ_BUFFER_LIMIT, input) == NULL)
        {
            free(ab.fields_types);
            free(ab.is_additional);
            free(ab.offsets);
            free(ab.field_names);
            errno = EIO;
            perror("Error while reading a line (AtomBuilder.atom_builder_new)");
        }
    while (strncmp(line, "ITEM: ATOMS", 11) != 0);

    fgets(line, READ_BUFFER_LIMIT, input);
    get_additional_types(line, &ab);

    initialize_functions(&ab);
    if (errno != 0)
    {
        free(ab.parsing_functions);
        free(ab.fields_types);
        free(ab.is_additional);
        free(ab.offsets);
        free(ab.field_names);
        return ab;
    }

    fseek(input, pos, SEEK_SET);
    return ab;
}

struct Atom read_atom_entry(const struct AtomBuilder ab,
                            char line[READ_BUFFER_LIMIT])
{
    struct Atom atom;
    atom.additionnal_fields = malloc(ab.N_additional * sizeof(union AtomField));
    if (atom.additionnal_fields == NULL)
    {
        errno = ENOMEM;
        perror("Error while allocating memory (Atom.additional_fields)");
        return atom;
    }

    char *field = strtok(line, " ");

    for (unsigned int f = 0; f < ab.N_fields; field = strtok(NULL, " "), f++)
    {
        union AtomField res = ab.parsing_functions[f](field);
        size_t offset = ab.offsets[f];
        if ((ab.is_additional)[f])
            (atom.additionnal_fields)[offset] = res;
        else
        {
            switch (ab.fields_types[f])
            {
                case AFT_INT:
                    {
                        int *ptr = (int *) ((void *) &atom + offset);
                        *ptr = res.i;
                        break;
                    }
                case AFT_DOUBLE:
                    {
                        double *ptr = (double *) ((void *) &atom + offset);
                        *ptr = res.d;
                        break;
                    }
                case AFT_STRING:
                    // Only if the field is `label`
                    strncpy(atom.label, res.s, LABEL_LIMIT);
                    break;
                default:
                    errno = EINVAL;
                    perror(
                        "Error while reading an entry "
                        "(AtomBuilder.new_atom_entry)");
                    return atom;
            }
        }
    }

    return atom;
}

void atom_builder_copy(struct AtomBuilder *dest, const struct AtomBuilder src)
{
    strncpy(dest->dump_format, src.dump_format, READ_BUFFER_LIMIT);

    dest->N_fields = src.N_fields;
    dest->N_additional = src.N_additional;

    dest->field_names = malloc(src.N_fields * sizeof(char[FIELD_NAME_LIMIT]));
    if (dest->field_names == NULL)
    {
        errno = ENOMEM;
        perror("Error while allocation memory (atom_builder_copy.dest.field_names)");
        return;
    }
    memcpy(dest->field_names, src.field_names, src.N_fields * sizeof(char[FIELD_NAME_LIMIT]));

    dest->offsets = malloc(src.N_fields * sizeof(size_t));
    if (dest->offsets == NULL)
    {
        free(dest->field_names);
        errno = ENOMEM;
        perror("Error while allocation memory (atom_builder_copy.dest.offsets)");
        return;
    }
    memcpy(dest->offsets, src.offsets, src.N_fields * sizeof(size_t));

    dest->is_additional = malloc(src.N_fields * sizeof(int));
    if (dest->is_additional == NULL)
    {
        free(dest->offsets);
        free(dest->field_names);
        errno = ENOMEM;
        perror("Error while allocation memory (atom_builder_copy.dest.is_additional)");
        return;
    }
    memcpy(dest->is_additional, src.is_additional, src.N_fields * sizeof(int));

    dest->fields_types = malloc(src.N_fields * sizeof(enum AtomFieldType));
    if (dest->fields_types == NULL)
    {
        free(dest->is_additional);
        free(dest->offsets);
        free(dest->field_names);
        errno = ENOMEM;
        perror("Error while allocation memory (atom_builder_copy.dest.fields_types)");
        return;
    }
    memcpy(dest->fields_types, src.fields_types, src.N_fields * sizeof(enum AtomFieldType));

    dest->parsing_functions = malloc(src.N_fields * sizeof(AtomBuilderParsingFunction));
    if (dest->parsing_functions == NULL)
    {
        free(dest->fields_types);
        free(dest->is_additional);
        free(dest->offsets);
        free(dest->field_names);
        errno = ENOMEM;
        perror("Error while allocation memory (atom_builder_copy.dest.parsing_functions)");
        return;
    }
    memcpy(dest->parsing_functions, src.parsing_functions, src.N_fields * sizeof(AtomBuilderParsingFunction));
}

void atom_builder_delete(struct AtomBuilder *ab)
{
    free(ab->parsing_functions);
    free(ab->field_names);
    free(ab->offsets);
    free(ab->is_additional);
    free(ab->fields_types);
}
