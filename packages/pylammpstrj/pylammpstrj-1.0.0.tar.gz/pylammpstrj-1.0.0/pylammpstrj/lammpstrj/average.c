#include <errno.h>
#include <stdbool.h>
#include <stddef.h>

#include "utils.h"

double *trajectory_average_property(const struct Trajectory trajectory, const unsigned int field)
{
    // Preparing the array
    double *averages = calloc(trajectory.N_configurations, sizeof(double));
    if (averages == NULL)
    {
        errno = ENOMEM;
        perror("Error while allocating memory (compute_average_property.averages)");
        return NULL;
    }

    // Transforming the field into an offset
    size_t offset = trajectory.atom_builder.offsets[field];

    // Getting the type of data
    enum AtomFieldType type = trajectory.atom_builder.fields_types[field];

    if (!trajectory.atom_builder.is_additional[field])
        for (unsigned int c = 0, i = 0; c < trajectory.N_configurations; c++)
        {
            for (unsigned int a = 0; a < trajectory.N_atoms[c]; a++, i++)
            {
                switch (type)
                {
                    case AFT_INT:
                        averages[c] += (double) *(int *) ((void *) (trajectory.atoms + i) + offset);
                        break;
                    case AFT_DOUBLE:
                        averages[c] += *(double *) ((void *) (trajectory.atoms + i) + offset);
                        break;
                    default:
                        free(averages);
                        errno = EINVAL;
                        perror("Error while selecting type of value");
                        return NULL;
                }
            }
            averages[c] /= trajectory.N_atoms[c];
        }
    else
        for (unsigned int c = 0, i = 0; c < trajectory.N_configurations; c++)
        {
            for (unsigned int a = 0; a < trajectory.N_atoms[c]; a++, i++)
            {
                switch (type)
                {
                    case AFT_INT:
                        averages[c] += (double) trajectory.atoms[i].additionnal_fields[offset].i;
                        break;
                    case AFT_DOUBLE:
                        averages[c] += trajectory.atoms[i].additionnal_fields[offset].d;
                        break;
                    default:
                        free(averages);
                        errno = EINVAL;
                        perror("Error while selecting type of value");
                        return NULL;
                }
            }
            averages[c] /= trajectory.N_atoms[c];
        }

    return averages;
}
