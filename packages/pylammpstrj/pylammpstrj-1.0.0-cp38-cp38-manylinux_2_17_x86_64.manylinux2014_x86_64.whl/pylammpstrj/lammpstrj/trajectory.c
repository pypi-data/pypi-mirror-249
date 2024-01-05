#include "utils.h"

#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void trajectory_init(struct Trajectory *trajectory,
                     struct AtomBuilder atom_builder,
                     unsigned long N_configurations, unsigned int *steps,
                     unsigned int *N_atoms, struct Box *box, struct Atom *atoms)
{
    trajectory->atom_builder = atom_builder;
    trajectory->N_configurations = N_configurations;
    trajectory->steps = steps;
    trajectory->N_atoms = N_atoms;
    trajectory->box = box;
    trajectory->atoms = atoms;
}

void delete_atoms(struct Trajectory *trajectory)
{
    for (unsigned int c = 0, i = 0; c < trajectory->N_configurations; c++)
        for (unsigned int a = 0; a < (trajectory->N_atoms)[c]; a++, i++)
            atom_delete(trajectory->atoms + i);
}

void trajectory_delete(struct Trajectory *trajectory)
{
    atom_builder_delete(&(trajectory->atom_builder));

    if (trajectory->atoms != NULL)
    {
        delete_atoms(trajectory);
        free(trajectory->atoms);
        trajectory->atoms = NULL;
    }

    if (trajectory->box != NULL)
    {
        free(trajectory->box);
        trajectory->box = NULL;
    }

    if (trajectory->steps != NULL)
    {
        free(trajectory->steps);
        trajectory->steps = NULL;
    }

    if (trajectory->N_atoms != NULL)
    {
        free(trajectory->N_atoms);
        trajectory->N_atoms = NULL;
    }
}
