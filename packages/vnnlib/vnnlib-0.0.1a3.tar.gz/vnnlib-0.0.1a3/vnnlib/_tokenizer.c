#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include "structmember.h"
#include <regex.h>

typedef struct
{
    PyObject_HEAD /**/
        int start_pos;
    int end_pos;
} MetaObject;

static int
Meta_init(MetaObject *self, PyObject *args, PyObject *kwds)
{
    static char *kwlist[] = {"start_pos", "end_pos", NULL};

    if (!PyArg_ParseTupleAndKeywords(args, kwds, "ii", kwlist, &self->start_pos, &self->end_pos))
    {
        return -1;
    }
    return 0;
}

static PyMemberDef Meta_members[] = {
    {"start_pos", T_INT, offsetof(MetaObject, start_pos), 0, NULL},
    {"end_pos", T_INT, offsetof(MetaObject, end_pos), 0, NULL},
    {NULL} /* Sentinel */
};

static PyTypeObject MetaType = {
    PyVarObject_HEAD_INIT(NULL, 0)
        .tp_name = "_tokenizer.Meta",
    .tp_basicsize = sizeof(MetaObject),
    .tp_itemsize = 0,
    .tp_flags = Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE,
    .tp_new = PyType_GenericNew,
    .tp_init = (initproc)Meta_init,
    .tp_members = Meta_members,
};

typedef struct
{
    PyObject_HEAD /**/
        PyObject *token_type;
    PyObject *value;
    PyObject *meta;
} TokenObject;

static int
Token_init(TokenObject *self, PyObject *args, PyObject *kwds)
{
    static char *kwlist[] = {"token_type", "value", "meta", NULL};

    if (!PyArg_ParseTupleAndKeywords(args, kwds, "OOO", kwlist, &self->token_type, &self->value, &self->meta))
    {
        return -1;
    }
    return 0;
}

static PyMemberDef Token_members[] = {
    {"token_type", T_OBJECT_EX, offsetof(TokenObject, token_type), 0, NULL},
    {"value", T_OBJECT_EX, offsetof(TokenObject, value), 0, NULL},
    {"meta", T_OBJECT_EX, offsetof(TokenObject, meta), 0, NULL},
    {NULL} /* Sentinel */
};

static PyTypeObject TokenType = {
    PyVarObject_HEAD_INIT(NULL, 0)
        .tp_name = "_tokenizer.Token",
    .tp_basicsize = sizeof(TokenObject),
    .tp_itemsize = 0,
    .tp_flags = Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE,
    .tp_new = PyType_GenericNew,
    .tp_init = (initproc)Token_init,
    .tp_members = Token_members,
};

typedef struct
{
    PyObject_HEAD const char *text;
    long int *textlen;
    long int i;
    int strict;
} _tokenizer;

static PyObject *tokenize(PyObject *self, PyObject *args, PyObject *kwargs)
{
    const char *text;
    long int *textlen;
    PyObject *skip;
    int *strict = 1;
    static char *kwlist[] = {"text", "skip", "strict", NULL};

    // Parse Args
    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "s#O!|p", kwlist, &text, &textlen, &PySet_Type, &skip, &strict))
        return NULL;

    // Quick check
    if (textlen == 0)
    {
        return PyLong_FromDouble(-10);
    }

    // Tokenize

    return PyLong_FromLong(textlen);
}

static PyMethodDef TokenizerMethods[] = {
    {"tokenize", tokenize, METH_VARARGS | METH_KEYWORDS, NULL},
    {NULL, NULL, 0, NULL} /* Sentinel */
};

static struct PyModuleDef tokenizermodule = {
    PyModuleDef_HEAD_INIT,
    "tokenizer", /* name of module */
    NULL,        /* module documentation, may be NULL */
    -1,          /* size of per-interpreter state of the module,
                    or -1 if the module keeps state in global variables. */
    TokenizerMethods};

PyMODINIT_FUNC
PyInit__tokenizer(void)
{
    PyObject *m;
    if (PyType_Ready(&MetaType) < 0)
        return NULL;
    if (PyType_Ready(&TokenType) < 0)
        return NULL;

    m = PyModule_Create(&tokenizermodule);
    if (m == NULL)
        return NULL;

    Py_INCREF(&MetaType);
    if (PyModule_AddObject(m, "Meta", (PyObject *)&MetaType) < 0)
    {
        Py_DECREF(&MetaType);
        Py_DECREF(m);
        return NULL;
    }

    Py_INCREF(&TokenType);
    if (PyModule_AddObject(m, "Token", (PyObject *)&TokenType) < 0)
    {
        Py_DECREF(&TokenType);
        Py_DECREF(m);
        return NULL;
    }

    PyObject *dummy_meta = PyObject_CallFunction((PyObject *)&MetaType, "ii", 0, 0);
    PyObject *dummy_token = PyObject_CallFunction((PyObject *)&TokenType, "ssO", "_", "", dummy_meta);
    if (PyModule_AddObject(m, "DUMMY", dummy_token) < 0)
    {
        Py_DECREF(&dummy_token);
        Py_DECREF(&dummy_meta);
        Py_DECREF(m);
        return NULL;
    }

    PyObject *eof_meta = PyObject_CallFunction((PyObject *)&MetaType, "ii", -1, -1);
    PyObject *eof_token = PyObject_CallFunction((PyObject *)&TokenType, "ssO", "EOF", "", eof_meta);
    if (PyModule_AddObject(m, "EOF", eof_token) < 0)
    {
        Py_DECREF(&eof_token);
        Py_DECREF(&eof_meta);
        Py_DECREF(m);
        return NULL;
    }

    return m;
}
