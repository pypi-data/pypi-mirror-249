#include <errno.h>
#include <stdbool.h>
#include <stddef.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "utils.h"

static bool less_than(union AtomField f1, enum AtomFieldType type,
                      const union AtomField f2)
{
    switch (type)
    {
        case AFT_INT:
            return f1.i < f2.i;
        case AFT_DOUBLE:
            return f1.d < f2.d;
        case AFT_STRING:
            return strcmp(f1.s, f2.s) < 0;
        default:
            errno = EINVAL;
            perror("Error while comparing fields");
            break;
    }
    return 0;
}

static bool less_than_equal_to(union AtomField f1, enum AtomFieldType type,
                               const union AtomField f2)
{
    switch (type)
    {
        case AFT_INT:
            return f1.i <= f2.i;
        case AFT_DOUBLE:
            return f1.d <= f2.d;
        case AFT_STRING:
            return strcmp(f1.s, f2.s) <= 0;
        default:
            errno = EINVAL;
            perror("Error while comparing fields");
            break;
    }
    return 0;
}

static bool equal_to(union AtomField f1, enum AtomFieldType type,
                     const union AtomField f2)
{
    switch (type)
    {
        case AFT_INT:
            return f1.i == f2.i;
        case AFT_DOUBLE:
            return f1.d == f2.d;
        case AFT_STRING:
            return strcmp(f1.s, f2.s) == 0;
        default:
            errno = EINVAL;
            perror("Error while comparing fields");
            break;
    }
    return 0;
}

static bool greater_than_equal_to(union AtomField f1, enum AtomFieldType type,
                                  const union AtomField f2)
{
    switch (type)
    {
        case AFT_INT:
            return f1.i >= f2.i;
        case AFT_DOUBLE:
            return f1.d >= f2.d;
        case AFT_STRING:
            return strcmp(f1.s, f2.s) >= 0;
        default:
            errno = EINVAL;
            perror("Error while comparing fields");
            break;
    }
    return 0;
}

static bool greater_than(union AtomField f1, enum AtomFieldType type,
                         const union AtomField f2)
{
    switch (type)
    {
        case AFT_INT:
            return f1.i > f2.i;
        case AFT_DOUBLE:
            return f1.d > f2.d;
        case AFT_STRING:
            return strcmp(f1.s, f2.s) > 0;
        default:
            errno = EINVAL;
            perror("Error while comparing fields");
            break;
    }
    return 0;
}

typedef bool (*select_function)(union AtomField, enum AtomFieldType,
                                const union AtomField);

select_function get_select_function(enum Operator op)
{
    switch (op)
    {
        case OPERATOR_LT:
            return &less_than;
        case OPERATOR_LEQ:
            return &less_than_equal_to;
        case OPERATOR_EQ:
            return &equal_to;
        case OPERATOR_GEQ:
            return &greater_than_equal_to;
        default:
            return &greater_than;
    }
}

void select_atoms(struct Trajectory *trajectory, const unsigned int field,
                  const enum Operator op, const union AtomField value,
                  const bool inplace, struct Trajectory *selected)
{
    // Preparing the arrays
    struct Box *boxes = NULL;
    unsigned int *steps = NULL;
    if (!inplace)
    {
        boxes = malloc(trajectory->N_configurations * sizeof(struct Box));
        if (boxes == NULL)
        {
            errno = ENOMEM;
            perror("Error while allocating memory (select_atoms.boxes)");
            return;
        }
        steps = malloc(trajectory->N_configurations * sizeof(unsigned int));
        if (steps == NULL)
        {
            free(boxes);
            errno = ENOMEM;
            perror("Error while allocating memory (select_atoms.steps)");
            return;
        }
        memcpy(steps, trajectory->steps,
               trajectory->N_configurations * sizeof(unsigned int));
    }

    unsigned int *N_atoms =
        calloc(trajectory->N_configurations, sizeof(unsigned int));
    if (N_atoms == NULL)
    {
        if (!inplace)
        {
            free(steps);
            free(boxes);
        }
        errno = ENOMEM;
        perror("Error while allocating memory (select_atoms.N_atoms)");
        return;
    }

    struct Atom *atoms = NULL;
    unsigned long atoms_size = 0;
    unsigned long total_atoms = 0;
    unsigned long total_selected = 0;

    // Transforming the `field` in an offset
    size_t offset = trajectory->atom_builder.offsets[field];

    // Transforming the `op` in a function
    enum AtomFieldType type = trajectory->atom_builder.fields_types[field];
    bool (*to_select)(union AtomField, enum AtomFieldType,
                      const union AtomField) = get_select_function(op);

    for (unsigned int c = 0; c < trajectory->N_configurations; c++)
    {
        // Deep copying the box
        if (!inplace) box_copy(boxes + c, trajectory->box[c]);

        // Allocating enough memory for the current configuration atoms
        {
            struct Atom *new_atoms =
                realloc(atoms, (atoms_size + trajectory->N_atoms[c]) *
                                   sizeof(struct Atom));
            if (new_atoms == NULL)  // Could not reallocate memory
            {
                for (unsigned int a = 0; a < total_selected; a++)
                    atom_delete(atoms + a);
                if (atoms != NULL) free(atoms);
                free(N_atoms);
                if (!inplace)
                {
                    free(steps);
                    free(boxes);
                }
                errno = ENOMEM;
                perror(
                    "Error while reallocating memory (select_atoms.new_atoms)");
                return;
            }
            atoms_size += trajectory->N_atoms[c];
            atoms = new_atoms;
        }

        // Actually selecting the atoms
        for (unsigned int a = 0; a < trajectory->N_atoms[c]; a++, total_atoms++)
        {
            union AtomField af;
            if (trajectory->atom_builder.is_additional[field])
                af = atoms[a].additionnal_fields[field];
            else
                switch (type)
                {
                    case AFT_INT:
                        af.i = *(
                            int *) ((void *) (trajectory->atoms + total_atoms) +
                                    offset);
                        break;
                    case AFT_DOUBLE:
                        af.d = *(double *) ((void *) (trajectory->atoms +
                                                      total_atoms) +
                                            offset);
                        break;
                    case AFT_STRING:
                        // Only the label
                        strncpy(af.s, trajectory->atoms[total_atoms].label,
                                LABEL_LIMIT);
                        break;
                    default:
                        for (unsigned int at = 0; at < total_selected; at++)
                            atom_delete(atoms + at);
                        if (atoms != NULL) free(atoms);
                        free(N_atoms);
                        if (!inplace)
                        {
                            free(steps);
                            free(boxes);
                        }
                        errno = EINVAL;
                        perror("Error while selecting the type");
                        return;
                }

            if (to_select(af, type, value))
            {
                atom_copy(atoms + total_selected, trajectory->atoms[total_atoms], trajectory->atom_builder);
                if (errno != 0)
                {
                    for (unsigned int at = 0; at < total_selected; at++)
                        atom_delete(atoms + at);
                    if (atoms != NULL) free(atoms);
                    free(N_atoms);
                    if (!inplace)
                    {
                        free(steps);
                        free(boxes);
                    }
                    errno = ENOMEM;
                    perror(
                        "Error while allocating memory "
                        "(select_atoms.atoms[].additionnal_fields)");
                    return;
                }
                N_atoms[c]++;
                total_selected++;
            }
        }

        // Reallocating the memory if needed
        if (total_selected >
            atoms_size)  // only if the arrays are not of same size
        {
            struct Atom *new_atoms =
                realloc(atoms, total_selected * sizeof(struct Atom));
            if (new_atoms == NULL)  // Could not reallocate memory
            {
                for (unsigned int a = 0; a < total_selected; a++)
                    atom_delete(atoms + a);
                if (atoms != NULL) free(atoms);
                free(N_atoms);
                if (!inplace)
                {
                    free(steps);
                    free(boxes);
                }
                errno = ENOMEM;
                perror(
                    "Error while reallocating memory (select_atoms.new_atoms)");
                return;
            }
            atoms_size = total_selected;
            atoms = new_atoms;
        }
    }

    if (!inplace)
    {
        // Deep copying the AtomBuilder
        struct AtomBuilder atom_builder;
        atom_builder_copy(&atom_builder, trajectory->atom_builder);

        if (errno != 0)
        {
            for (unsigned int a = 0; a < total_selected; a++)
                atom_delete(atoms + a);
            if (atoms != NULL) free(atoms);
            free(N_atoms);
            if (!inplace)
            {
                free(steps);
                free(boxes);
            }
            errno = ENOMEM;
            perror("Error while allocating memory (select_atoms.atom_builder_copy)");
            return;
        }

        // Finally, creating the new trajectory
        trajectory_init(selected, atom_builder, trajectory->N_configurations,
                        steps, N_atoms, boxes, atoms);
    }
    else
    {
        // Only need to copy the new N_atoms and new atoms
        free(trajectory->N_atoms);
        trajectory->N_atoms = N_atoms;

        // Freeing the old atoms and saving the new pointer
        for (unsigned int a = 0; a < total_atoms; a++)
            atom_delete(trajectory->atoms + a);
        free(trajectory->atoms);
        trajectory->atoms = atoms;
    }
}
