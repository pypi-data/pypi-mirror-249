/**
 * \file
 * Contains the utilities' prototypes and definitions.
 *
 * Contains the trajectory, box, atom definitions as well as
 * their `define`s, and their functions.
 */
#ifndef _UTILS_H
#define _UTILS_H

#include <stddef.h>
#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>

/**
 * The maximum number of characters of element names.
 *
 * The value is 3 for 2 characters and the null-terminator.
 */
#define LABEL_LIMIT 3
/**
 * The maximum number of characters to read for element strings.
 *
 * The null-terminator is excluded.
 */
#define LABEL_SCANF_LIMIT "2"
/**
 * The maximum number of bonds.
 *
 * It is set to four because we only study systems containing H, O, Na and C.
 */
#define N_MAX_BONDS 4

enum AtomFieldType
{
    AFT_NULL,
    AFT_INT,
    AFT_DOUBLE,
    AFT_STRING
};

#define ATOM_FIELD_STR_LIMIT 10

union AtomField
{
    int i;
    double d;
    char s[ATOM_FIELD_STR_LIMIT];
};

/**
 * The data structure used to represent atoms.
 *
 * The atoms are identified by their `id`.
 *
 * This data structure holds the informations about an atom's `label`,
 * `position`, and `charge`.
 */
struct Atom
{
    unsigned int id;
    unsigned int type;
    char label[LABEL_LIMIT];
    double position[3];
    double charge;

    union AtomField *additionnal_fields;
};

void atom_delete(struct Atom *atom);

/** The maximum number of characters read at once. */
#define READ_BUFFER_LIMIT 128

#define FIELD_NAME_LIMIT 15

typedef union AtomField (*AtomBuilderParsingFunction)(const char[READ_BUFFER_LIMIT]);

struct AtomBuilder
{
    char dump_format[READ_BUFFER_LIMIT];

    unsigned int N_fields;
    unsigned int N_additional;
    char (*field_names)[FIELD_NAME_LIMIT];  // A pointer to static arrays
    size_t *offsets;
    int *is_additional;
    enum AtomFieldType *fields_types;
    AtomBuilderParsingFunction *parsing_functions;
};

void atom_copy(struct Atom *, const struct Atom, const struct AtomBuilder);

struct AtomBuilder atom_builder_new(const char *dump_format, FILE *input);

struct Atom read_atom_entry(const struct AtomBuilder ab,
                            char line[READ_BUFFER_LIMIT]);

void atom_builder_copy(struct AtomBuilder *, const struct AtomBuilder);

void atom_builder_delete(struct AtomBuilder *ab);

/** An enum to compare `Atom`s properties. */
enum Operator
{
    OPERATOR_LT,
    OPERATOR_LEQ,
    OPERATOR_EQ,
    OPERATOR_GEQ,
    OPERATOR_GT
};

/**
 * The length of the `Box` flag.
 *
 * The flag is in the format "xx xx xx". The extra character is the
 * null-terminator.
 */
#define BOX_FLAG_LIMIT 9
/** The length of the `Box` flag read by `scanf`. */
#define BOX_FLAG_SCANF_LIMIT "8"
/** The size of the array that stores the `Box`'s limits. */
#define BOX_BOUNDS_LIMIT 6

/** The data structure used to represent a simulation box. */
struct Box
{
    char flag[BOX_FLAG_LIMIT];
    double bounds[BOX_BOUNDS_LIMIT];
};

/** Creating an instance of `Box` based on the attributes provided. */
struct Box box_new(char flag[BOX_FLAG_LIMIT], double bounds[BOX_BOUNDS_LIMIT]);

void box_copy(struct Box *dest, const struct Box src);

/** The data structure used to represent a trajectory. */
struct Trajectory
{
    struct AtomBuilder atom_builder;
    unsigned long N_configurations;
    unsigned int *N_atoms;
    unsigned int *steps;
    struct Box *box;
    struct Atom *atoms;
};

void trajectory_init(struct Trajectory *trajectory, struct AtomBuilder atom_builder, 
                     unsigned long N_configurations, unsigned int *N_atoms,
                     unsigned int *steps,
                     struct Box *box, struct Atom *atoms);

/**
 * Select atoms from a group of atoms based on a condition over one of their
 * properties.
 *
 * @param[in] N_atoms the number of atoms in the input array.
 * @param[in] atoms the input `Atom` array.
 * @param[in] select the selection function.
 * @param[in] value the value to which the atoms property is compared.
 * @param[out] the number of selected atoms.
 *
 * @return an array of `Atom`s of size `N_selected`.
 *
 * @sa {lower_than .. greater_than}.
 */
void select_atoms(struct Trajectory *trajectory, const unsigned int field,
                  const enum Operator op, const union AtomField value, const bool inplace,
                  struct Trajectory *selected);

/**
 * To compute a set of atoms' average `property`.
 *
 * @param[in] N_atoms the number of atoms in the array.
 * @param[in] atoms the `Atom`s array.
 *
 * @return the average of the property over the set of atoms.
 */
double *trajectory_average_property(const struct Trajectory, const unsigned int);

void trajectory_delete(struct Trajectory *trajectory);

/** The base size of the array that stores the configurations. */
#define READ_N_CONFIGURATIONS_BASE_SIZE 1000

/** The size increment of the array that stores the configurations. */
#define READ_N_CONFIGURATIONS_INCREMENT 1000

void trajectory_read(const char *file_name, const unsigned long start,
                     char dump_format[READ_BUFFER_LIMIT],
                     struct Trajectory *trajectory);

void trajectory_skip(FILE *input, const unsigned long start);

#endif
