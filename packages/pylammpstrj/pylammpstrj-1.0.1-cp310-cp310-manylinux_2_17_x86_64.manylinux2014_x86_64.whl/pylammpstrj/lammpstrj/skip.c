#include "utils.h"

#include <errno.h>
#include <omp.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void trajectory_skip(FILE *input, const unsigned long start)
{
    unsigned long current_step = 0, starting_pos;
    unsigned int N_atoms;
    char dump[READ_BUFFER_LIMIT];

    // Skipping the first configurations
    do
    {
        starting_pos = ftell(input);

        // Reading the current timestep
        if (fscanf(input,
                   "ITEM: TIMESTEP %lu ITEM: NUMBER OF ATOMS %u ITEM: BOX "
                   "BOUNDS %*" BOX_FLAG_SCANF_LIMIT
                   "c %*f %*f %*f %*f %*f %*f",
                   &current_step, &N_atoms) != 2)
        {
            errno = EINVAL;
            perror("Error while scanning a line");
            return;
        }

        if (fgets(dump, READ_BUFFER_LIMIT, input) == NULL)
        {
            errno = EIO;
            perror("Error while dumping the dumping format");
            return;
        }

        if (current_step >= start)
        {
            // Returning to the start position
            fseek(input, starting_pos, SEEK_SET);
            break;
        }

        // Skipping the atom entries
        for (unsigned int a = 0; a < N_atoms; a++)
        {
            if (fgets(dump, READ_BUFFER_LIMIT, input) == NULL)
            {
                errno = EIO;
                perror("Error while dumping an atom entry");
                return;
            }
        }
    }
    while (current_step < start);
}
