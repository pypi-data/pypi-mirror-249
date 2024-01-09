#include "utils.h"

#include <string.h>

// To build a new box
struct Box box_new(char flag[BOX_FLAG_LIMIT], double bounds[BOX_BOUNDS_LIMIT])
{
    struct Box box;
    for (unsigned int c = 0; c < BOX_FLAG_LIMIT - 1; c++)
        box.flag[c] = flag[c];
    box.flag[BOX_FLAG_LIMIT - 1] = '\0';
    for (unsigned int b = 0; b < BOX_BOUNDS_LIMIT; b++)
        box.bounds[b] = bounds[b];
    return box;
}

// To copy a box to another
void box_copy(struct Box *dest, const struct Box src)
{
    strncpy(dest->flag, src.flag, BOX_FLAG_LIMIT * sizeof(char));
    memcpy(dest->bounds, src.bounds, BOX_BOUNDS_LIMIT * sizeof(double));
}
