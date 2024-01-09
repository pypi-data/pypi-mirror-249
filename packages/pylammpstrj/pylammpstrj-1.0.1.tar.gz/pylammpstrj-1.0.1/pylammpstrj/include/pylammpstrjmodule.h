#ifndef PYLAMMPSTRJMODULE_H
#define PYLAMMPSTRJMODULE_H

#include <Python.h>

#include "utils.h"

typedef struct PyTrajectoryObject
{
    PyObject_HEAD
    struct Trajectory trajectory;
}
PyTrajectoryObject;

typedef struct PyBoxObject
{
    PyObject_HEAD
    struct Box box;
}
PyBoxObject;

typedef struct PyAtomObject
{
    PyObject_HEAD
    PyTrajectoryObject *trajectory;
    struct Atom atom;
}
PyAtomObject;

#endif
