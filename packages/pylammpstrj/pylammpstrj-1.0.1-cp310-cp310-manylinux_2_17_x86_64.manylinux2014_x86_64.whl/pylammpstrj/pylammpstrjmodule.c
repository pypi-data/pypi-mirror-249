#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include <abstract.h>
#include <boolobject.h>
#include <descrobject.h>
#include <listobject.h>
#include <object.h>
#include <structmember.h>
#include <unicodeobject.h>
#include <floatobject.h>
#include <longobject.h>
#include <pyerrors.h>
#include <modsupport.h>
#include <methodobject.h>
#include <pymacro.h>
#include <warnings.h>

#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <stddef.h>
#include <string.h>

#include "pylammpstrjmodule.h"
#include "utils.h"

/*
 *  Atom
 */
static void PyAtom_dealloc(PyAtomObject *self)
{
    Py_TYPE(self)->tp_free((PyObject *) self);
}

static PyObject *PyAtom_new(PyTypeObject *type, PyObject *Py_UNUSED(args),
                                  PyObject *Py_UNUSED(kwargs))
{
    PyAtomObject *self;
    self = (PyAtomObject *) type->tp_alloc(type, 0);
    return (PyObject *) self;
}

static PyObject *PyAtom_get_id(PyAtomObject *self, void *Py_UNUSED(closure))
{
        return PyLong_FromUnsignedLong(self->atom.id);
}

static PyObject *PyAtom_get_type(PyAtomObject *self, void *Py_UNUSED(closure))
{
        return PyLong_FromUnsignedLong(self->atom.type);
}

static PyObject *PyAtom_get_label(PyAtomObject *self, void *Py_UNUSED(closure))
{
        return PyUnicode_FromString(self->atom.label);
}

static PyObject *PyAtom_get_x(PyAtomObject *self, void *Py_UNUSED(closure))
{
        return PyFloat_FromDouble(self->atom.position[0]);
}

static PyObject *PyAtom_get_y(PyAtomObject *self, void *Py_UNUSED(closure))
{
        return PyFloat_FromDouble(self->atom.position[1]);
}

static PyObject *PyAtom_get_z(PyAtomObject *self, void *Py_UNUSED(closure))
{
        return PyFloat_FromDouble(self->atom.position[2]);
}

static PyObject *PyAtom_get_charge(PyAtomObject *self, void *Py_UNUSED(closure))
{
        return PyFloat_FromDouble(self->atom.charge);
}

static PyObject *PyAtom_get_additional_fields(PyAtomObject *self, void *Py_UNUSED(closure))
{
    struct AtomBuilder atom_builder = self->trajectory->trajectory.atom_builder;
    PyObject *list = PyList_New(atom_builder.N_additional);
    for (unsigned int f = 0, f_add = 0; f < atom_builder.N_fields; f++)
    {
        if (!atom_builder.is_additional[f])
            continue;
        size_t offset = atom_builder.offsets[f];
        switch (atom_builder.fields_types[f])
        {
            case AFT_INT:
                PyList_SetItem(list, f_add, PyLong_FromLong(self->atom.additionnal_fields[offset].i));
                break;
            case AFT_DOUBLE:
                PyList_SetItem(list, f_add, PyFloat_FromDouble(self->atom.additionnal_fields[offset].d));
                break;
            case AFT_STRING:
                PyList_SetItem(list, f_add, PyUnicode_FromString(self->atom.additionnal_fields[offset].s));
                break;
            default:
                printf("Error: AFT_NULL");
                PyList_SetItem(list, f_add, Py_None);
                break;
        }
        f_add++;
    }

    return (PyObject *) list;
}

static PyGetSetDef PyAtom_getset[] = {
    {.name = "id",
        .get = (getter) PyAtom_get_id,
     .doc = "The names of the fields."},
    {.name = "type",
        .get = (getter) PyAtom_get_type,
     .doc = "The additionnal fields."},
    {.name = "label",
        .get = (getter) PyAtom_get_label,
     .doc = "The dump format."},
    {.name = "x",
        .get = (getter) PyAtom_get_x,
     .doc = "The number of configurations"},
    {.name = "y",
        .get = (getter) PyAtom_get_y,
     .doc = "The number of configurations"},
    {.name = "z",
        .get = (getter) PyAtom_get_z,
     .doc = "The dump format."},
    {.name = "charge",
        .get = (getter) PyAtom_get_charge,
     .doc = "The charge."},
    {.name = "additional_fields",
        .get = (getter) PyAtom_get_additional_fields,
     .doc = "The additional fields."},
    {NULL}};

static PyObject *PyAtom_str(PyAtomObject *self)
{
    return PyUnicode_FromFormat("[%lu %lu %s %S %S %S %S %S]",
            self->atom.id,
            self->atom.type,
            self->atom.label,
            PyObject_Str(PyAtom_get_x(self, NULL)),
            PyObject_Str(PyAtom_get_y(self, NULL)),
            PyObject_Str(PyAtom_get_z(self, NULL)),
            PyObject_Str(PyAtom_get_charge(self, NULL)),
            PyObject_Str(PyAtom_get_additional_fields(self, NULL)));
}

static PyObject *PyAtom_repr(PyAtomObject *self)
{
    return PyUnicode_FromFormat("atom(id=%lu type=%lu label='%s' x=%S y=%S z=%S charge=%S additional_fields=%S])",
            self->atom.id,
            self->atom.type,
            self->atom.label,
            PyObject_Str(PyAtom_get_x(self, NULL)),
            PyObject_Str(PyAtom_get_y(self, NULL)),
            PyObject_Str(PyAtom_get_z(self, NULL)),
            PyObject_Str(PyAtom_get_charge(self, NULL)),
            PyObject_Str(PyAtom_get_additional_fields(self, NULL)));
}

static PyTypeObject PyAtomType =
{
    PyVarObject_HEAD_INIT(NULL, 0).tp_name = "pylammpstrj.PyAtom",
    .tp_doc = "Atom objects",
    .tp_basicsize = sizeof(PyAtomObject),
    .tp_itemsize = 0,
    .tp_flags = Py_TPFLAGS_DEFAULT,
    .tp_dealloc = (destructor) PyAtom_dealloc,
    .tp_new = PyAtom_new,
    .tp_getset = PyAtom_getset,
    .tp_str = (reprfunc) PyAtom_str,
    .tp_repr = (reprfunc) PyAtom_repr
};

static void PyAtom_initialize(PyAtomObject *self, PyTrajectoryObject *trajectory, struct Atom atom)
{
    self->trajectory = trajectory;
    self->atom = atom;
}

/*
 *  Box
 */
static void PyBox_dealloc(PyBoxObject *self)
{
    Py_TYPE(self)->tp_free((PyObject *) self);
}

static PyObject *PyBox_new(PyTypeObject *type, PyObject *Py_UNUSED(args),
        PyObject *Py_UNUSED(kwargs))
{
    PyBoxObject *self;
    self = (PyBoxObject *) type->tp_alloc(type, 0);
    return (PyObject *) self;
}

static PyObject *PyBox_get_bounds(PyBoxObject *self, PyObject *Py_UNUSED(closure))
{
    PyObject *list = PyList_New(6);
    for (unsigned int b = 0; b < 6; b++)
        PyList_SetItem(list, b, PyFloat_FromDouble(self->box.bounds[b]));
    return list;
}

static PyObject *PyBox_get_flag(PyBoxObject *self, PyObject *Py_UNUSED(closure))
{
    return PyUnicode_FromString(self->box.flag);
}

static PyGetSetDef PyBox_getset[] = {
    {.name = "bounds",
        .get = (getter) PyBox_get_bounds,
     .doc = "The box bounds."},
    {.name = "flags",
        .get = (getter) PyBox_get_flag,
        .doc = "The box flag."},
    {NULL, NULL, NULL, NULL, NULL}};

static PyObject *PyBox_str(PyBoxObject *self)
{
    return PyUnicode_FromFormat("[%S '%s']",
            PyObject_Str(PyBox_get_bounds(self, NULL)),
            self->box.flag);
}

static PyObject *PyBox_repr(PyBoxObject *self)
{
    return PyUnicode_FromFormat("box(bounds=%S flag='%s')",
            PyObject_Str(PyBox_get_bounds(self, NULL)),
            self->box.flag);
}

static void PyBox_initialize(PyBoxObject *self, struct Box box)
{
    self->box = box;
}

static PyTypeObject PyBoxType =
{
    PyVarObject_HEAD_INIT(NULL, 0).tp_name = "pylammpstrj.PyBox",
    .tp_doc = "Box objects",
    .tp_basicsize = sizeof(PyBoxObject),
    .tp_itemsize = 0,
    .tp_flags = Py_TPFLAGS_DEFAULT,
    .tp_dealloc = (destructor) PyBox_dealloc,
    .tp_new = PyBox_new,
    .tp_getset = PyBox_getset,
    .tp_str = (reprfunc) PyBox_str,
    .tp_repr = (reprfunc) PyBox_repr
};

/*
 *  Trajectory
 */
static void PyTrajectory_dealloc(PyTrajectoryObject *self)
{
    trajectory_delete(&(self->trajectory));
    Py_TYPE(self)->tp_free((PyObject *) self);
}

static PyObject *PyTrajectory_new(PyTypeObject *type, PyObject *Py_UNUSED(args),
                                  PyObject *Py_UNUSED(kwargs))
{
    PyTrajectoryObject *self;
    self = (PyTrajectoryObject *) type->tp_alloc(type, 0);
    return (PyObject *) self;
}

static PyObject *PyTrajectory_get_N_configurations(PyTrajectoryObject *self, void *Py_UNUSED(closure))
{
    return (PyObject *) PyLong_FromLong(self->trajectory.N_configurations);
}

static PyObject *PyTrajectory_get_steps(PyTrajectoryObject *self, void *Py_UNUSED(closure))
{
    PyObject *list = PyList_New(self->trajectory.N_configurations);
    for (unsigned int c = 0; c < self->trajectory.N_configurations; c++)
        PyList_SetItem(list, c, PyLong_FromLong(self->trajectory.steps[c]));
    return list;
}

static PyObject *PyTrajectory_get_N_atoms(PyTrajectoryObject *self, void *Py_UNUSED(closure))
{
    PyObject *list = PyList_New(self->trajectory.N_configurations);
    for (unsigned int c = 0; c < self->trajectory.N_configurations; c++)
        PyList_SetItem(list, c,
                       PyLong_FromLong(self->trajectory.N_atoms[c]));
    return list;
}

static PyObject *PyTrajectory_get_dump_format(PyTrajectoryObject *self,
                                               void *Py_UNUSED(closure))
{
    return PyUnicode_FromString((self->trajectory).atom_builder.dump_format);
}

static PyObject *PyTrajectory_get_field_names(PyTrajectoryObject *self,
                                               void *Py_UNUSED(closure))
{
    PyObject *list = PyList_New(self->trajectory.atom_builder.N_fields);
    for (unsigned int f = 0; f < self->trajectory.atom_builder.N_fields; f++)
        PyList_SetItem(
            list, f, PyUnicode_FromString(self->trajectory.atom_builder.field_names[f]));
    return list;
}

static PyObject *PyTrajectory_get_additional_fields(PyTrajectoryObject *self,
                                                 void *Py_UNUSED(closure))
{
    PyObject *list = PyList_New(self->trajectory.atom_builder.N_additional);
    struct AtomBuilder atom_builder = self->trajectory.atom_builder;
    for (unsigned int f = 0, fa = 0; f < self->trajectory.atom_builder.N_fields; f++)
    {
        if (!atom_builder.is_additional[f])
            continue;
        PyList_SetItem(list, fa,
                       PyUnicode_FromString(self->trajectory.atom_builder.field_names[f]));
        fa++;
    }
    return list;
}

static PyObject *PyTrajectory_get_atoms(PyTrajectoryObject *self, void *Py_UNUSED(closure))
{
    PyObject *list = PyList_New(self->trajectory.N_configurations);
    for (unsigned int c = 0, at = 0; c < self->trajectory.N_configurations; c++)
    {
        PyObject *inner_list = PyList_New(self->trajectory.N_atoms[c]);
        for (unsigned int a = 0; a < self->trajectory.N_atoms[c]; a++, at++)
        {
            PyAtomObject *atom = (PyAtomObject *) PyAtom_new(&PyAtomType, NULL, NULL);
            PyAtom_initialize(atom, self, self->trajectory.atoms[at]);
            PyList_SetItem(inner_list, a, (PyObject *) atom);
        }
        PyList_SetItem(list, c, inner_list);
    }
    return list;
}

static PyObject *PyTrajectory_get_boxes(PyTrajectoryObject *self, void *Py_UNUSED(closure))
{
    PyObject *list = PyList_New(self->trajectory.N_configurations);
    for (unsigned int c = 0; c < self->trajectory.N_configurations; c++)
    {
        PyBoxObject *box = (PyBoxObject *) PyBox_new(&PyBoxType, NULL, NULL);
        PyBox_initialize(box, self->trajectory.box[c]);
        PyList_SetItem(list, c, (PyObject *) box);
    }
    return list;
}

static PyGetSetDef PyTrajectory_getset[] = {
    {.name = "N_configurations",
        .get = (getter) PyTrajectory_get_N_configurations,
     .doc = "The number of configurations"},
    {.name = "steps",
        .get = (getter) PyTrajectory_get_steps,
        .doc = "The timesteps."},
    {.name = "N_atoms",
        .get = (getter) PyTrajectory_get_N_atoms,
     .doc = "The number of configurations"},
    {.name = "dump_format",
        .get = (getter) PyTrajectory_get_dump_format,
     .doc = "The dump format."},
    {.name = "field_names",
        .get = (getter) PyTrajectory_get_field_names,
     .doc = "The names of the fields."},
    {.name = "additional_fields",
        .get = (getter) PyTrajectory_get_additional_fields,
     .doc = "The additionnal fields."},
    {.name = "atoms",
        .get = (getter) PyTrajectory_get_atoms,
     .doc = "The atoms."},
    {.name = "boxes",
        .get = (getter) PyTrajectory_get_boxes,
        .doc = "The boxes."},
    {NULL, NULL, NULL, NULL, NULL}};

static PyObject *PyTrajectory_str(PyTrajectoryObject *self)
{
    return PyUnicode_FromFormat("[%lu, %S, %s, %S, %S, %R]",
            self->trajectory.N_configurations,
            PyObject_Str(PyTrajectory_get_N_atoms(self, NULL)),
            self->trajectory.atom_builder.dump_format,
            PyObject_Str(PyTrajectory_get_field_names(self, NULL)),
            PyObject_Str(PyTrajectory_get_additional_fields(self, NULL)),
            PyObject_Repr(PyTrajectory_get_atoms(self, NULL)));
}

static PyObject *PyTrajectory_repr(PyTrajectoryObject *self)
{
    return PyUnicode_FromFormat("trajectory(N_configurations=%lu N_atoms=%S dump_format='%s' field_names=%S is_additional=%S atoms=%R)",
            self->trajectory.N_configurations,
            PyObject_Str(PyTrajectory_get_N_atoms(self, NULL)),
            self->trajectory.atom_builder.dump_format,
            PyObject_Str(PyTrajectory_get_field_names(self, NULL)),
            PyObject_Str(PyTrajectory_get_additional_fields(self, NULL)),
            PyObject_Repr(PyTrajectory_get_atoms(self, NULL)));
}

enum Operator parse_operator(const long input_op)
{
    enum Operator op = (enum Operator) input_op;
    if (op < 0 || 4 < op)  // Assuming there are only 4 comparison operators
        PyErr_SetString(PyExc_RuntimeError, "Invalid operator: pylammpstrj operators should be used.");
    return op;
}

unsigned int parse_field_name(const struct AtomBuilder atom_builder, const char *field_name)
{
    for (unsigned int f = 0; f < atom_builder.N_fields; f++)
        if (strcmp(field_name, atom_builder.field_names[f]) == 0)
            return f;
    PyErr_SetString(PyExc_RuntimeError, "Attribute does not match any attribute.");
    return 0;
}

union AtomField parse_value(const struct AtomBuilder atom_builder, const unsigned int field, PyObject *input_value)
{
    enum AtomFieldType type = atom_builder.fields_types[field];
    union AtomField value = {0};
    if (PyObject_TypeCheck(input_value, &PyLong_Type) && type == AFT_INT) // Only accepts PyLong
        value.i = (int) PyLong_AsLong(input_value);
    else if (type == AFT_DOUBLE) // if double then accept PyFloat and PyLong for convenience
    {
        if (PyObject_TypeCheck(input_value, &PyFloat_Type))
            value.d =  PyFloat_AsDouble(input_value);
        else if (PyObject_TypeCheck(input_value, &PyLong_Type))
        {
            PyErr_Warn(PyExc_UserWarning, "value cast from 'int' to 'float'");
            value.d = PyLong_AsDouble(input_value);
        }
        else
            PyErr_SetString(PyExc_RuntimeError, "Argument value does not match attribute type.");
    }
    else if (PyObject_TypeCheck(input_value, &PyUnicode_Type) && type == AFT_STRING)
        strncpy(value.s, PyUnicode_AsUTF8(input_value), LABEL_LIMIT);
    else
        PyErr_SetString(PyExc_RuntimeError, "Argument value does not match attribute type.");
    return value;
}

static void PyTrajectory_initialize(PyTrajectoryObject *self, struct Trajectory trajectory)
{
    self->trajectory = trajectory;
}

static PyObject *PyTrajectory_select_atoms(PyTrajectoryObject *self, PyObject *args, PyObject *kwargs)
{
    char *kwlist[] = {"", "", "", "inplace", NULL};
    unsigned int field;
    enum Operator op;
    union AtomField value;
    char *field_name;
    long input_op;
    PyObject *input_value; // Needs to be freed?
    int inplace = false;

    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "siO|$p", kwlist, &field_name,
                                     &input_op, &input_value, &inplace))
        return NULL;

    field = parse_field_name(self->trajectory.atom_builder, field_name);
    if (PyErr_Occurred())
        return NULL;
    op = parse_operator(input_op);
    if (PyErr_Occurred())
        return NULL;
    value = parse_value(self->trajectory.atom_builder, field, input_value);
    if (PyErr_Occurred())
        return NULL;

    PyTrajectoryObject *new = (PyTrajectoryObject *) PyTrajectory_new(Py_TYPE(self), NULL, NULL);
    struct Trajectory trajectory;
    if (!inplace)
    {
        select_atoms(&(self->trajectory), field, op, value, false, &trajectory);
        if (errno != 0)
            return PyErr_SetFromErrno(PyExc_RuntimeError);
        PyTrajectory_initialize(new, trajectory);
        return (PyObject *) new;
    }

    select_atoms(&(self->trajectory), field, op, value, true, NULL);
    if (errno != 0)
        return PyErr_SetFromErrno(PyExc_RuntimeError);
    // Need to return None otherwise it segfaults if the result is not assigned
    return Py_None;
}

static PyObject *PyTrajectory_compute_average(PyTrajectoryObject *self, PyObject *args)
{
    char *field_name;
    if (!PyArg_ParseTuple(args, "s", &field_name))
        return NULL;
    unsigned int field = parse_field_name(self->trajectory.atom_builder, field_name);
    if (PyErr_Occurred())
        return NULL;
    double *averages = trajectory_average_property(self->trajectory, field);
    if (errno != 0)
        return PyErr_SetFromErrno(PyExc_RuntimeError);

    // Instanciating the return list
    PyObject *list = PyList_New(self->trajectory.N_configurations);
    if (list == NULL)
        return list;
    for (unsigned int c = 0; c < self->trajectory.N_configurations; c++)
        PyList_SetItem(list, c, PyFloat_FromDouble(averages[c]));
    free(averages);
    return list;
}

static PyMethodDef PyTrajectory_methods[] =
{
    {"select_atoms", (PyCFunction) PyTrajectory_select_atoms, METH_VARARGS | METH_KEYWORDS, "Select atoms."},
    {"average_property", (PyCFunction) PyTrajectory_compute_average, METH_VARARGS, "Computes the average of an atomic property throughout the simulation."},
    {NULL, NULL, 0, NULL}
};

static PyTypeObject PyTrajectoryType =
{
    PyVarObject_HEAD_INIT(NULL, 0).tp_name = "pylammpstrj.PyTrajectory",
    .tp_doc = "Trajectory objects",
    .tp_basicsize = sizeof(PyTrajectoryObject),
    .tp_itemsize = 0,
    .tp_flags = Py_TPFLAGS_DEFAULT,
    .tp_dealloc = (destructor) PyTrajectory_dealloc,
    .tp_new = PyTrajectory_new,
    .tp_getset = PyTrajectory_getset,
    .tp_methods = PyTrajectory_methods,
    .tp_str = (reprfunc) PyTrajectory_str,
    .tp_repr = (reprfunc) PyTrajectory_repr
};

static PyObject *pylammpstrj_read(PyObject *Py_UNUSED(self), PyObject *args,
                                  PyObject *kwds)
{
    char *kwlist[] = {"", "start", "dump_format", NULL};
    const char *file_name;
    const unsigned long start = 0;
    char *dump_format = NULL;

    if (!PyArg_ParseTupleAndKeywords(args, kwds, "s|$is", kwlist, &file_name,
                                     &start, &dump_format))
        return NULL;

    PyTrajectoryObject *pytrajectory = (PyTrajectoryObject *) PyTrajectory_new(&PyTrajectoryType, NULL, NULL);
    struct Trajectory trajectory;
    trajectory_read(file_name, start, dump_format, &trajectory);
    if (errno != 0)
        return PyErr_SetFromErrno(PyExc_RuntimeError);
    PyTrajectory_initialize(pytrajectory, trajectory);

    return (PyObject *) pytrajectory;
}

static PyMethodDef pylammpstrj_methods[] =
{
    {"read", (PyCFunction) pylammpstrj_read, METH_VARARGS | METH_KEYWORDS,
     "Read a trajectory file."},
    {NULL, NULL, 0, NULL}
};

static struct PyModuleDef pylammpstrjmodule = 
{
    .m_base = PyModuleDef_HEAD_INIT,
    .m_name = "pylammpstrj",
    .m_doc = "A module to read and process LAMMPS trajectory files.",
    .m_size = -1,
    .m_methods = pylammpstrj_methods
};

PyMODINIT_FUNC PyInit_pylammpstrj(void)
{
    PyObject *m;

    if (PyType_Ready(&PyAtomType) < 0)
        return NULL;
    if (PyType_Ready(&PyBoxType) < 0)
        return NULL;
    if (PyType_Ready(&PyTrajectoryType) < 0)
        return NULL;

    m = PyModule_Create(&pylammpstrjmodule);
    if (m == NULL)
        return NULL;

    Py_INCREF(&PyAtomType);
    if (PyModule_AddObject(m, "PyAtom", (PyObject *) &PyAtomType) < 0)
    {
        Py_DECREF(&PyAtomType);
        Py_DECREF(&m);
        return NULL;
    }

    Py_INCREF(&PyBoxType);
    if (PyModule_AddObject(m, "PyBox", (PyObject *) &PyBoxType) < 0)
    {
        Py_DECREF(&PyBoxType);
        Py_DECREF(&PyAtomType);
        Py_DECREF(&m);
        return NULL;
    }

    Py_INCREF(&PyTrajectoryType);
    if (PyModule_AddObject(m, "PyTrajectory", (PyObject *) &PyTrajectoryType) < 0)
    {
        Py_DECREF(&PyTrajectoryType);
        Py_DECREF(&PyBoxType);
        Py_DECREF(&PyAtomType);
        Py_DECREF(&m);
        return NULL;
    }

    // Module constants
    PyModule_AddIntConstant(m, "LESS_THAN", (long) OPERATOR_LT);
    PyModule_AddIntConstant(m, "LESS_THAN_EQUAL_TO", (long) OPERATOR_LEQ);
    PyModule_AddIntConstant(m, "EQUAL_TO", (long) OPERATOR_EQ);
    PyModule_AddIntConstant(m, "GREATER_THAN_EQUAL_TO", (long) OPERATOR_GEQ);
    PyModule_AddIntConstant(m, "GREATER_THAN", (long) OPERATOR_GT);

    return m;
}

