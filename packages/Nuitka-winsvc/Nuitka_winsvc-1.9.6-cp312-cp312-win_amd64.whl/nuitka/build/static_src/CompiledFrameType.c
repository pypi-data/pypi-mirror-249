//     Copyright 2023, Kay Hayen, mailto:kay.hayen@gmail.com
//
//     Part of "Nuitka", an optimizing Python compiler that is compatible and
//     integrates with CPython, but also works on its own.
//
//     Licensed under the Apache License, Version 2.0 (the "License");
//     you may not use this file except in compliance with the License.
//     You may obtain a copy of the License at
//
//        http://www.apache.org/licenses/LICENSE-2.0
//
//     Unless required by applicable law or agreed to in writing, software
//     distributed under the License is distributed on an "AS IS" BASIS,
//     WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
//     See the License for the specific language governing permissions and
//     limitations under the License.
//
#ifdef __IDE_ONLY__
#include "nuitka/freelists.h"
#include "nuitka/prelude.h"
#include <structmember.h>
#endif

// For reporting about reference counts per type.
#if _DEBUG_REFCOUNTS
int count_active_Nuitka_Frame_Type = 0;
int count_allocated_Nuitka_Frame_Type = 0;
int count_released_Nuitka_Frame_Type = 0;
#endif

// For reporting about frame cache usage
#if _DEBUG_REFCOUNTS
int count_active_frame_cache_instances = 0;
int count_allocated_frame_cache_instances = 0;
int count_released_frame_cache_instances = 0;
int count_hit_frame_cache_instances = 0;
#endif

#if PYTHON_VERSION < 0x3b0
static PyMemberDef Nuitka_Frame_memberlist[] = {
    {(char *)"f_back", T_OBJECT, offsetof(PyFrameObject, f_back), READONLY | RESTRICTED},
    {(char *)"f_code", T_OBJECT, offsetof(PyFrameObject, f_code), READONLY | RESTRICTED},
    {(char *)"f_builtins", T_OBJECT, offsetof(PyFrameObject, f_builtins), READONLY | RESTRICTED},
    {(char *)"f_globals", T_OBJECT, offsetof(PyFrameObject, f_globals), READONLY | RESTRICTED},
    {(char *)"f_lasti", T_INT, offsetof(PyFrameObject, f_lasti), READONLY | RESTRICTED},
    {NULL}};

#else
#define Nuitka_Frame_memberlist 0
#endif

#if PYTHON_VERSION < 0x300

static PyObject *Nuitka_Frame_get_exc_traceback(struct Nuitka_FrameObject *frame) {
    PyObject *result = frame->m_frame.f_exc_traceback;

    if (result == NULL) {
        result = Py_None;
    }

    Py_INCREF(result);
    return result;
}

static int Nuitka_Frame_set_exc_traceback(struct Nuitka_FrameObject *frame, PyObject *traceback) {
    Py_XDECREF(frame->m_frame.f_exc_traceback);

    if (traceback == Py_None) {
        traceback = NULL;
    }

    frame->m_frame.f_exc_traceback = traceback;
    Py_XINCREF(traceback);

    return 0;
}

static PyObject *Nuitka_Frame_get_exc_type(struct Nuitka_FrameObject *frame) {
    PyObject *result;

    if (frame->m_frame.f_exc_type != NULL) {
        result = frame->m_frame.f_exc_type;
    } else {
        result = Py_None;
    }

    Py_INCREF(result);
    return result;
}

static int Nuitka_Frame_set_exc_type(struct Nuitka_FrameObject *frame, PyObject *exception_type) {
    PyObject *old = frame->m_frame.f_exc_type;

    if (exception_type == Py_None) {
        exception_type = NULL;
    }

    frame->m_frame.f_exc_type = exception_type;
    Py_XINCREF(frame->m_frame.f_exc_type);

    Py_XDECREF(old);

    return 0;
}

static PyObject *Nuitka_Frame_get_exc_value(struct Nuitka_FrameObject *frame) {
    PyObject *result;

    if (frame->m_frame.f_exc_value != NULL) {
        result = frame->m_frame.f_exc_value;
    } else {
        result = Py_None;
    }

    Py_INCREF(result);
    return result;
}

static int Nuitka_Frame_set_exc_value(struct Nuitka_FrameObject *frame, PyObject *exception_value) {
    PyObject *old = frame->m_frame.f_exc_value;

    if (exception_value == Py_None) {
        exception_value = NULL;
    }

    frame->m_frame.f_exc_value = exception_value;
    Py_XINCREF(exception_value);
    Py_XDECREF(old);

    return 0;
}

static PyObject *Nuitka_Frame_get_restricted(struct Nuitka_FrameObject *frame, void *closure) {
    Py_INCREF(Py_False);
    return Py_False;
}

#endif

static PyObject *Nuitka_Frame_getlocals(struct Nuitka_FrameObject *nuitka_frame, void *closure) {
    if (nuitka_frame->m_type_description == NULL) {
#if PYTHON_VERSION < 0x3b0
        PyFrameObject *locals_owner = &nuitka_frame->m_frame;
#else
        _PyInterpreterFrame *locals_owner = &nuitka_frame->m_interpreter_frame;
#endif

        if (locals_owner->f_locals == NULL) {
            locals_owner->f_locals = MAKE_DICT_EMPTY();
        }

        Py_INCREF(locals_owner->f_locals);
        return locals_owner->f_locals;
    } else {
        PyObject *result = MAKE_DICT_EMPTY();
        PyObject **var_names = Nuitka_GetCodeVarNames(Nuitka_GetFrameCodeObject(nuitka_frame));

        char const *w = nuitka_frame->m_type_description;
        char const *t = nuitka_frame->m_locals_storage;

        while (*w != 0) {
            switch (*w) {
            case NUITKA_TYPE_DESCRIPTION_OBJECT:
            case NUITKA_TYPE_DESCRIPTION_OBJECT_PTR: {
                PyObject *value = *(PyObject **)t;
                CHECK_OBJECT_X(value);

                if (value != NULL) {
                    DICT_SET_ITEM(result, *var_names, value);
                }

                t += sizeof(PyObject *);

                break;
            }
            case NUITKA_TYPE_DESCRIPTION_CELL: {
                struct Nuitka_CellObject *value = *(struct Nuitka_CellObject **)t;
                assert(Nuitka_Cell_Check((PyObject *)value));
                CHECK_OBJECT(value);

                if (value->ob_ref != NULL) {
                    DICT_SET_ITEM(result, *var_names, value->ob_ref);
                }

                t += sizeof(struct Nuitka_CellObject *);

                break;
            }
            case NUITKA_TYPE_DESCRIPTION_NULL: {
                break;
            }
            case NUITKA_TYPE_DESCRIPTION_BOOL: {
                int value = *(int *)t;
                t += sizeof(int);
                switch ((nuitka_bool)value) {
                case NUITKA_BOOL_TRUE: {
                    DICT_SET_ITEM(result, *var_names, Py_True);
                    break;
                }
                case NUITKA_BOOL_FALSE: {
                    DICT_SET_ITEM(result, *var_names, Py_False);
                    break;
                }
                default:
                    break;
                }
                break;
            }
            default:
                assert(false);
            }

            w += 1;
            var_names += 1;
        }

        return result;
    }
}

static PyObject *Nuitka_Frame_getlineno(struct Nuitka_FrameObject *frame, void *closure) {
    return PyInt_FromLong(frame->m_frame.f_lineno);
}

static PyObject *Nuitka_Frame_gettrace(struct Nuitka_FrameObject *frame, void *closure) {
    PyObject *result = frame->m_frame.f_trace;
    Py_INCREF(result);
    return result;
}

static int Nuitka_Frame_settrace(struct Nuitka_FrameObject *frame, PyObject *v, void *closure) {
    PyThreadState *tstate = PyThreadState_GET();

    SET_CURRENT_EXCEPTION_TYPE0_STR(tstate, PyExc_RuntimeError, "f_trace is not writable in Nuitka");
    return -1;
}

#if PYTHON_VERSION >= 0x370
static PyObject *Nuitka_Frame_gettracelines(struct Nuitka_FrameObject *frame, void *closure) {
    PyObject *result = Py_False;
    Py_INCREF(result);
    return result;
}

static int Nuitka_Frame_settracelines(struct Nuitka_FrameObject *frame, PyObject *v, void *closure) {
    PyThreadState *tstate = PyThreadState_GET();

    SET_CURRENT_EXCEPTION_TYPE0_STR(tstate, PyExc_RuntimeError, "f_trace_lines is not writable in Nuitka");
    return -1;
}

static PyObject *Nuitka_Frame_gettraceopcodes(struct Nuitka_FrameObject *frame, void *closure) {
    PyObject *result = Py_False;
    Py_INCREF(result);
    return result;
}

static int Nuitka_Frame_settraceopcodes(struct Nuitka_FrameObject *frame, PyObject *v, void *closure) {
    PyThreadState *tstate = PyThreadState_GET();

    SET_CURRENT_EXCEPTION_TYPE0_STR(tstate, PyExc_RuntimeError, "f_trace_opcodes is not writable in Nuitka");
    return -1;
}
#endif

#if PYTHON_VERSION >= 0x3b0
static PyObject *Nuitka_Frame_getback(struct Nuitka_FrameObject *frame, void *closure) {
    return (PyObject *)PyFrame_GetBack(&frame->m_frame);
}
#endif

static PyGetSetDef Nuitka_Frame_getsetlist[] = {
    {(char *)"f_locals", (getter)Nuitka_Frame_getlocals, NULL, NULL},
    {(char *)"f_lineno", (getter)Nuitka_Frame_getlineno, NULL, NULL},
    {(char *)"f_trace", (getter)Nuitka_Frame_gettrace, (setter)Nuitka_Frame_settrace, NULL},
#if PYTHON_VERSION < 0x300
    {(char *)"f_restricted", (getter)Nuitka_Frame_get_restricted, NULL, NULL},
    {(char *)"f_exc_traceback", (getter)Nuitka_Frame_get_exc_traceback, (setter)Nuitka_Frame_set_exc_traceback, NULL},
    {(char *)"f_exc_type", (getter)Nuitka_Frame_get_exc_type, (setter)Nuitka_Frame_set_exc_type, NULL},
    {(char *)"f_exc_value", (getter)Nuitka_Frame_get_exc_value, (setter)Nuitka_Frame_set_exc_value, NULL},
#endif
#if PYTHON_VERSION >= 0x370
    {(char *)"f_trace_lines", (getter)Nuitka_Frame_gettracelines, (setter)Nuitka_Frame_settracelines, NULL},
    {(char *)"f_trace_opcodes", (getter)Nuitka_Frame_gettraceopcodes, (setter)Nuitka_Frame_settraceopcodes, NULL},
#endif
#if PYTHON_VERSION >= 0x3b0
    {(char *)"f_trace_lines", (getter)Nuitka_Frame_getback, NULL, NULL},
#endif
    {NULL}};

// tp_repr slot, decide how a function shall be output
static PyObject *Nuitka_Frame_tp_repr(struct Nuitka_FrameObject *nuitka_frame) {

#if PYTHON_VERSION >= 0x370
    PyCodeObject *code_object = Nuitka_GetFrameCodeObject(nuitka_frame);
    return Nuitka_String_FromFormat("<compiled_frame at %p, file %R, line %d, code %S>", nuitka_frame,
                                    code_object->co_filename, Nuitka_GetFrameLineNumber(nuitka_frame),
                                    code_object->co_name);
#elif _DEBUG_FRAME || _DEBUG_REFRAME || _DEBUG_EXCEPTIONS
    PyCodeObject *code_object = Nuitka_GetFrameCodeObject(nuitka_frame);
    return Nuitka_String_FromFormat("<compiled_frame object for %s at %p>",
                                    Nuitka_String_AsString(code_object->co_name), nuitka_frame);
#else
    return Nuitka_String_FromFormat("<compiled_frame object at %p>", nuitka_frame);
#endif
}

static void Nuitka_Frame_tp_clear(struct Nuitka_FrameObject *frame) {
    if (frame->m_type_description) {
        char const *w = frame->m_type_description;
        char const *t = frame->m_locals_storage;

        while (*w != 0) {
            switch (*w) {
            case NUITKA_TYPE_DESCRIPTION_OBJECT:
            case NUITKA_TYPE_DESCRIPTION_OBJECT_PTR: {
                PyObject *value = *(PyObject **)t;
                CHECK_OBJECT_X(value);

                Py_XDECREF(value);

                t += sizeof(PyObject *);

                break;
            }
            case NUITKA_TYPE_DESCRIPTION_CELL: {
                struct Nuitka_CellObject *value = *(struct Nuitka_CellObject **)t;
                assert(Nuitka_Cell_Check((PyObject *)value));
                CHECK_OBJECT(value);

                Py_DECREF(value);

                t += sizeof(struct Nuitka_CellObject *);

                break;
            }
            case NUITKA_TYPE_DESCRIPTION_NULL: {
                break;
            }
            case NUITKA_TYPE_DESCRIPTION_BOOL: {
                t += sizeof(int);

                break;
            }
            default:
                assert(false);
            }

            w += 1;
        }

        frame->m_type_description = NULL;
    }
}

#define MAX_FRAME_FREE_LIST_COUNT 100
static struct Nuitka_FrameObject *free_list_frames = NULL;
static int free_list_frames_count = 0;

static void Nuitka_Frame_tp_dealloc(struct Nuitka_FrameObject *nuitka_frame) {
#if _DEBUG_REFCOUNTS
    count_active_Nuitka_Frame_Type -= 1;
    count_released_Nuitka_Frame_Type += 1;
#endif

#ifndef __NUITKA_NO_ASSERT__
    // Save the current exception, if any, we must to not corrupt it.
    PyThreadState *tstate = PyThreadState_GET();

    PyObject *save_exception_type, *save_exception_value;
    PyTracebackObject *save_exception_tb;
    FETCH_ERROR_OCCURRED(tstate, &save_exception_type, &save_exception_value, &save_exception_tb);
    RESTORE_ERROR_OCCURRED(tstate, save_exception_type, save_exception_value, save_exception_tb);
#endif

    Nuitka_GC_UnTrack(nuitka_frame);

    PyFrameObject *frame = &nuitka_frame->m_frame;
#if PYTHON_VERSION < 0x3b0
    PyFrameObject *locals_owner = frame;
#else
    _PyInterpreterFrame *locals_owner = &nuitka_frame->m_interpreter_frame;
#endif

    Py_XDECREF(frame->f_back);
    Py_DECREF(locals_owner->f_builtins);
    Py_DECREF(locals_owner->f_globals);
    Py_XDECREF(locals_owner->f_locals);

#if PYTHON_VERSION < 0x370
    Py_XDECREF(frame->f_exc_type);
    Py_XDECREF(frame->f_exc_value);
    Py_XDECREF(frame->f_exc_traceback);
#endif

    Nuitka_Frame_tp_clear(nuitka_frame);

#if PYTHON_VERSION >= 0x3b0
    // Restore from backup, see header comment for the field "m_ob_size" to get
    // it.
    Py_SET_SIZE(nuitka_frame, nuitka_frame->m_ob_size);
#endif

    releaseToFreeList(free_list_frames, nuitka_frame, MAX_FRAME_FREE_LIST_COUNT);

#ifndef __NUITKA_NO_ASSERT__
    assert(tstate->curexc_type == save_exception_type);
    assert(tstate->curexc_value == save_exception_value);
    assert((PyTracebackObject *)tstate->curexc_traceback == save_exception_tb);
#endif
}

static int Nuitka_Frame_tp_traverse(struct Nuitka_FrameObject *frame, visitproc visit, void *arg) {
    Py_VISIT(frame->m_frame.f_back);

#if PYTHON_VERSION < 0x3b0
    PyFrameObject *locals_owner = &frame->m_frame;
#else
    _PyInterpreterFrame *locals_owner = &frame->m_interpreter_frame;
#endif

    Py_VISIT(locals_owner->f_builtins);
    Py_VISIT(locals_owner->f_globals);
    // Py_VISIT(locals_owner->f_locals);

#if PYTHON_VERSION < 0x370
    Py_VISIT(frame->m_frame.f_exc_type);
    Py_VISIT(frame->m_frame.f_exc_value);
    Py_VISIT(frame->m_frame.f_exc_traceback);
#endif

    // Traverse attached locals too.
    char const *w = frame->m_type_description;
    char const *t = frame->m_locals_storage;

    while (w != NULL && *w != 0) {
        switch (*w) {
        case NUITKA_TYPE_DESCRIPTION_OBJECT:
        case NUITKA_TYPE_DESCRIPTION_OBJECT_PTR: {
            PyObject *value = *(PyObject **)t;
            CHECK_OBJECT_X(value);

            Py_VISIT(value);
            t += sizeof(PyObject *);

            break;
        }
        case NUITKA_TYPE_DESCRIPTION_CELL: {
            struct Nuitka_CellObject *value = *(struct Nuitka_CellObject **)t;
            assert(Nuitka_Cell_Check((PyObject *)value));
            CHECK_OBJECT(value);

            Py_VISIT(value);

            t += sizeof(struct Nuitka_CellObject *);

            break;
        }
        case NUITKA_TYPE_DESCRIPTION_NULL: {
            break;
        }
        case NUITKA_TYPE_DESCRIPTION_BOOL: {
            t += sizeof(int);

            break;
        }
        default:
            assert(false);
        }

        w += 1;
    }

    return 0;
}

#if PYTHON_VERSION >= 0x340

static PyObject *Nuitka_Frame_clear(struct Nuitka_FrameObject *frame) {
    PyThreadState *tstate = PyThreadState_GET();

    if (Nuitka_Frame_IsExecuting(frame)) {
        SET_CURRENT_EXCEPTION_TYPE0_STR(tstate, PyExc_RuntimeError, "cannot clear an executing frame");

        return NULL;
    }

#if PYTHON_VERSION >= 0x3b0
    if (frame->m_frame_state == FRAME_COMPLETED) {
        Nuitka_Frame_tp_clear(frame);

        Py_RETURN_NONE;
    }

    if (frame->m_frame_state == FRAME_EXECUTING) {
        SET_CURRENT_EXCEPTION_TYPE0_STR(tstate, PyExc_RuntimeError, "cannot clear an executing frame");
        return NULL;
    }
#endif

#if PYTHON_VERSION >= 0x340
    // For frames that are closed, we also need to close the generator.
    PyObject *f_gen = Nuitka_GetFrameGenerator(frame);
    if (f_gen != NULL) {
        CHECK_OBJECT(f_gen);

        Py_INCREF(frame);

        bool close_exception;

        if (Nuitka_Generator_Check(f_gen)) {
            struct Nuitka_GeneratorObject *generator = (struct Nuitka_GeneratorObject *)f_gen;
            Nuitka_SetFrameGenerator(frame, NULL);

            close_exception = !_Nuitka_Generator_close(tstate, generator);
        }
#if PYTHON_VERSION >= 0x350
        else if (Nuitka_Coroutine_Check(f_gen)) {
            struct Nuitka_CoroutineObject *coroutine = (struct Nuitka_CoroutineObject *)f_gen;
            Nuitka_SetFrameGenerator(frame, NULL);

            close_exception = !_Nuitka_Coroutine_close(tstate, coroutine);
        }
#endif
#if PYTHON_VERSION >= 0x360
        else if (Nuitka_Asyncgen_Check(f_gen)) {
            struct Nuitka_AsyncgenObject *asyncgen = (struct Nuitka_AsyncgenObject *)f_gen;
            Nuitka_SetFrameGenerator(frame, NULL);

            close_exception = !_Nuitka_Asyncgen_close(tstate, asyncgen);
        }
#endif
        else {
            // Compiled frames should only have our types, so this ought to not happen.
            assert(false);

            Nuitka_SetFrameGenerator(frame, NULL);

            close_exception = false;
        }

        if (unlikely(close_exception)) {
            PyErr_WriteUnraisable(f_gen);
        }

        Py_DECREF(frame);
    }
#endif

    Nuitka_Frame_tp_clear(frame);

    Py_RETURN_NONE;
}

#endif

static inline Py_ssize_t Nuitka_Frame_GetSize(struct Nuitka_FrameObject *frame) {
#if PYTHON_VERSION < 0x3b0
    return Py_SIZE(frame);
#else
    return frame->m_ob_size;
#endif
}

static PyObject *Nuitka_Frame_sizeof(struct Nuitka_FrameObject *frame) {
    return PyInt_FromSsize_t(sizeof(struct Nuitka_FrameObject) + Py_SIZE(frame));
}

static PyMethodDef Nuitka_Frame_methods[] = {
#if PYTHON_VERSION >= 0x340
    {"clear", (PyCFunction)Nuitka_Frame_clear, METH_NOARGS, "F.clear(): clear most references held by the frame"},
#endif
    {"__sizeof__", (PyCFunction)Nuitka_Frame_sizeof, METH_NOARGS, "F.__sizeof__() -> size of F in memory, in bytes"},
    {NULL, NULL}};

PyTypeObject Nuitka_Frame_Type = {
    PyVarObject_HEAD_INIT(NULL, 0) "compiled_frame",
    sizeof(struct Nuitka_FrameObject),
    1,
    (destructor)Nuitka_Frame_tp_dealloc,     // tp_dealloc
    0,                                       // tp_print
    0,                                       // tp_getattr
    0,                                       // tp_setattr
    0,                                       // tp_compare
    (reprfunc)Nuitka_Frame_tp_repr,          // tp_repr
    0,                                       // tp_as_number
    0,                                       // tp_as_sequence
    0,                                       // tp_as_mapping
    0,                                       // tp_hash
    0,                                       // tp_call
    0,                                       // tp_str
    0,                                       // tp_getattro (PyObject_GenericGetAttr)
    0,                                       // tp_setattro (PyObject_GenericSetAttr)
    0,                                       // tp_as_buffer
    Py_TPFLAGS_DEFAULT | Py_TPFLAGS_HAVE_GC, // tp_flags
    0,                                       // tp_doc
    (traverseproc)Nuitka_Frame_tp_traverse,  // tp_traverse
    (inquiry)Nuitka_Frame_tp_clear,          // tp_clear
    0,                                       // tp_richcompare
    0,                                       // tp_weaklistoffset
    0,                                       // tp_iter
    0,                                       // tp_iternext
    Nuitka_Frame_methods,                    // tp_methods
    Nuitka_Frame_memberlist,                 // tp_members
    Nuitka_Frame_getsetlist,                 // tp_getset
    0,                                       // tp_base
    0,                                       // tp_dict
};

void _initCompiledFrameType(void) {
    assert(Nuitka_Frame_Type.tp_doc != PyFrame_Type.tp_doc || PyFrame_Type.tp_doc == NULL);
    assert(Nuitka_Frame_Type.tp_traverse != PyFrame_Type.tp_traverse);
    assert(Nuitka_Frame_Type.tp_clear != PyFrame_Type.tp_clear || PyFrame_Type.tp_clear == NULL);
    assert(Nuitka_Frame_Type.tp_richcompare != PyFrame_Type.tp_richcompare || PyFrame_Type.tp_richcompare == NULL);
    assert(Nuitka_Frame_Type.tp_weaklistoffset != PyFrame_Type.tp_weaklistoffset ||
           PyFrame_Type.tp_weaklistoffset == 0);
    assert(Nuitka_Frame_Type.tp_iter != PyFrame_Type.tp_iter || PyFrame_Type.tp_iter == NULL);
    assert(Nuitka_Frame_Type.tp_iternext != PyFrame_Type.tp_iternext || PyFrame_Type.tp_iternext == NULL);
    assert(Nuitka_Frame_Type.tp_methods != PyFrame_Type.tp_methods);
    assert(Nuitka_Frame_Type.tp_members != PyFrame_Type.tp_members);
    assert(Nuitka_Frame_Type.tp_getset != PyFrame_Type.tp_getset);
    assert(Nuitka_Frame_Type.tp_dict != PyFrame_Type.tp_dict);
    assert(Nuitka_Frame_Type.tp_descr_get != PyFrame_Type.tp_descr_get || PyFrame_Type.tp_descr_get == NULL);

    assert(Nuitka_Frame_Type.tp_descr_set != PyFrame_Type.tp_descr_set || PyFrame_Type.tp_descr_set == NULL);
    assert(Nuitka_Frame_Type.tp_dictoffset != PyFrame_Type.tp_dictoffset || PyFrame_Type.tp_dictoffset == 0);
    // TODO: These get changed and into the same thing, not sure what to compare against, project something
    // assert(Nuitka_Frame_Type.tp_init != PyFrame_Type.tp_init || PyFrame_Type.tp_init == NULL);
    // assert(Nuitka_Frame_Type.tp_alloc != PyFrame_Type.tp_alloc || PyFrame_Type.tp_alloc == NULL);
    // assert(Nuitka_Frame_Type.tp_new != PyFrame_Type.tp_new || PyFrame_Type.tp_new == NULL);
    // assert(Nuitka_Frame_Type.tp_free != PyFrame_Type.tp_free || PyFrame_Type.tp_free == NULL);
    assert(Nuitka_Frame_Type.tp_bases != PyFrame_Type.tp_bases);
    assert(Nuitka_Frame_Type.tp_mro != PyFrame_Type.tp_mro);
    assert(Nuitka_Frame_Type.tp_cache != PyFrame_Type.tp_cache || PyFrame_Type.tp_cache == NULL);
    assert(Nuitka_Frame_Type.tp_subclasses != PyFrame_Type.tp_subclasses || PyFrame_Type.tp_cache == NULL);
    assert(Nuitka_Frame_Type.tp_weaklist != PyFrame_Type.tp_weaklist);
    assert(Nuitka_Frame_Type.tp_del != PyFrame_Type.tp_del || PyFrame_Type.tp_del == NULL);
#if PYTHON_VERSION >= 0x340
    assert(Nuitka_Frame_Type.tp_finalize != PyFrame_Type.tp_finalize || PyFrame_Type.tp_finalize == NULL);
#endif
    Nuitka_PyType_Ready(&Nuitka_Frame_Type, &PyFrame_Type, true, true, false, false, false);

    // These are to be used interchangeably. Make sure that's true.
    assert(offsetof(struct Nuitka_FrameObject, m_frame) == 0);
}

static struct Nuitka_FrameObject *_MAKE_COMPILED_FRAME(PyCodeObject *code, PyObject *module, PyObject *f_locals,
                                                       Py_ssize_t locals_size) {
    CHECK_CODE_OBJECT(code);
    CHECK_OBJECT(module);

#if _DEBUG_REFCOUNTS
    count_active_Nuitka_Frame_Type += 1;
    count_allocated_Nuitka_Frame_Type += 1;
#endif

    PyObject *globals = ((PyModuleObject *)module)->md_dict;
    CHECK_OBJECT(globals);

    assert(PyDict_Check(globals));

    struct Nuitka_FrameObject *result;

    // Macro to assign result memory from GC or free list.
    allocateFromFreeList(free_list_frames, struct Nuitka_FrameObject, Nuitka_Frame_Type, locals_size);

    result->m_type_description = NULL;

    PyFrameObject *frame = &result->m_frame;
    // Globals and locals are stored differently before Python 3.11
#if PYTHON_VERSION < 0x3b0
    PyFrameObject *locals_owner = frame;
#else
    _PyInterpreterFrame *locals_owner = &result->m_interpreter_frame;
#endif

    locals_owner->f_code = code;

    frame->f_trace = Py_None;

#if PYTHON_VERSION < 0x370
    frame->f_exc_type = NULL;
    frame->f_exc_value = NULL;
    frame->f_exc_traceback = NULL;
#else
    frame->f_trace_lines = 0;
    frame->f_trace_opcodes = 0;
#endif

#if PYTHON_VERSION >= 0x3b0
    result->m_ob_size = Py_SIZE(result);
#endif
    frame->f_back = NULL;

    Py_INCREF(dict_builtin);
    locals_owner->f_builtins = (PyObject *)dict_builtin;

    Py_INCREF(globals);
    locals_owner->f_globals = globals;

    // Note: Reference taking happens in calling function.
    CHECK_OBJECT_X(f_locals);
    locals_owner->f_locals = f_locals;

#if PYTHON_VERSION < 0x340
    frame->f_tstate = PyThreadState_GET();
#endif

#if PYTHON_VERSION < 0x3b0
    frame->f_lasti = -1;
    frame->f_iblock = 0;
#endif

    frame->f_lineno = code->co_firstlineno;

#if PYTHON_VERSION >= 0x340
    Nuitka_SetFrameGenerator(result, NULL);

    Nuitka_Frame_MarkAsNotExecuting(result);
#endif

#if PYTHON_VERSION >= 0x3b0
    result->m_interpreter_frame.frame_obj = &result->m_frame;
    result->m_interpreter_frame.owner = 0;
    result->m_interpreter_frame.prev_instr = _PyCode_CODE(code);
    result->m_frame.f_frame = &result->m_interpreter_frame;
#endif

    Nuitka_GC_Track(result);
    return result;
}

struct Nuitka_FrameObject *MAKE_MODULE_FRAME(PyCodeObject *code, PyObject *module) {
    PyObject *f_locals = ((PyModuleObject *)module)->md_dict;
    Py_INCREF(f_locals);

    return _MAKE_COMPILED_FRAME(code, module, f_locals, 0);
}

struct Nuitka_FrameObject *MAKE_FUNCTION_FRAME(PyThreadState *tstate, PyCodeObject *code, PyObject *module,
                                               Py_ssize_t locals_size) {
    PyObject *f_locals;

    if (likely((code->co_flags & CO_OPTIMIZED) == CO_OPTIMIZED)) {
        f_locals = NULL;
    } else {
        PyObject *kw_pairs[2] = {const_str_plain___module__, MODULE_NAME0(tstate, module)};
        f_locals = MAKE_DICT(kw_pairs, 1);
    }

    return _MAKE_COMPILED_FRAME(code, module, f_locals, locals_size);
}

struct Nuitka_FrameObject *MAKE_CLASS_FRAME(PyThreadState *tstate, PyCodeObject *code, PyObject *module,
                                            PyObject *f_locals, Py_ssize_t locals_size) {
    // The frame template sets f_locals on usage itself, need not create it that way.
    if (f_locals == NULL) {
        PyObject *kw_pairs[2] = {const_str_plain___module__, MODULE_NAME0(tstate, module)};
        f_locals = MAKE_DICT(kw_pairs, 1);
    } else {
        Py_INCREF(f_locals);
    }

    return _MAKE_COMPILED_FRAME(code, module, f_locals, locals_size);
}

// This is the backend of MAKE_CODE_OBJECT macro.
PyCodeObject *makeCodeObject(PyObject *filename, int line, int flags, PyObject *function_name,
#if PYTHON_VERSION >= 0x3b0
                             PyObject *function_qualname,
#endif
                             PyObject *argnames, PyObject *freevars, int arg_count
#if PYTHON_VERSION >= 0x300
                             ,
                             int kw_only_count
#endif
#if PYTHON_VERSION >= 0x380
                             ,
                             int pos_only_count
#endif
) {
    CHECK_OBJECT(filename);
    assert(Nuitka_String_CheckExact(filename));
    CHECK_OBJECT(function_name);
    assert(Nuitka_String_CheckExact(function_name));

    if (argnames == NULL) {
        argnames = const_tuple_empty;
    }
    CHECK_OBJECT(argnames);
    assert(PyTuple_Check(argnames));

    if (freevars == NULL) {
        freevars = const_tuple_empty;
    }
    CHECK_OBJECT(freevars);
    assert(PyTuple_Check(freevars));

    // The PyCode_New has funny code that interns, mutating the tuple that owns
    // it. Really serious non-immutable shit. We have triggered that changes
    // behind our back in the past.
#ifndef __NUITKA_NO_ASSERT__
    // TODO: Reactivate once code object creation becomes un-streaming driven
    // and we can pass the extra args with no worries.

    // Py_hash_t hash = DEEP_HASH(argnames);
#endif

#if PYTHON_VERSION < 0x300
    PyObject *code = const_str_empty;
    PyObject *lnotab = const_str_empty;
#else
#if PYTHON_VERSION < 0x3b0
    PyObject *code = const_bytes_empty;
    PyObject *lnotab = const_bytes_empty;
#else
    // Our code object needs to be recognizable, and Python doesn't store the
    // length anymore, so we need a non-empty one.
    static PyObject *empty_code = NULL;
    if (empty_code == NULL) {
        empty_code = PyBytes_FromString("\0\0");
    }
    PyObject *code = empty_code;
    static PyObject *lnotab = NULL;
    if (lnotab == NULL) {
        lnotab = PyBytes_FromStringAndSize("\x80\x00\xd8\x04\x08\x80"
                                           "D",
                                           7);
    }
#endif
#endif

    // For Python 3.11 this value is checked, even if not used.
#if PYTHON_VERSION >= 0x3b0
    int nlocals = (int)PyTuple_GET_SIZE(argnames);
#else
    int nlocals = 0;
#endif

    // Not using PyCode_NewEmpty, it doesn't given us much beyond this
    // and is not available for Python2.

#if PYTHON_VERSION >= 0x380
    PyCodeObject *result = PyCode_NewWithPosOnlyArgs(arg_count, // argcount
#else
    PyCodeObject *result = PyCode_New(arg_count, // argcount
#endif

#if PYTHON_VERSION >= 0x300
#if PYTHON_VERSION >= 0x380
                                                     pos_only_count, // kw-only count
#endif
                                                     kw_only_count, // kw-only count
#endif
                                                     nlocals,           // nlocals
                                                     0,                 // stacksize
                                                     flags,             // flags
                                                     code,              // code (bytecode)
                                                     const_tuple_empty, // consts (we are not going to be compatible)
                                                     const_tuple_empty, // names (we are not going to be compatible)
                                                     argnames,          // varnames (we are not going to be compatible)
                                                     freevars,          // freevars
                                                     const_tuple_empty, // cellvars (we are not going to be compatible)
                                                     filename,          // filename
                                                     function_name,     // name
#if PYTHON_VERSION >= 0x3b0
                                                     function_qualname, // qualname
#endif
                                                     line,  // firstlineno (offset of the code object)
                                                     lnotab // lnotab (table to translate code object)
#if PYTHON_VERSION >= 0x3b0
                                                     ,
                                                     const_bytes_empty // exceptiontable
#endif
    );

    // assert(DEEP_HASH(tstate, argnames) == hash);

    if (result == NULL) {
        PyErr_PrintEx(0);
    }

    CHECK_OBJECT(result);
    return result;
}

void Nuitka_Frame_AttachLocals(struct Nuitka_FrameObject *frame_object, char const *type_description, ...) {
    assertFrameObject(frame_object);

#if _DEBUG_FRAME
    PRINT_FORMAT("Attaching to frame 0x%lx %s\n", frame_object,
                 Nuitka_String_AsString(PyObject_Repr((PyObject *)Nuitka_Frame_GetCodeObject(&frame_object->m_frame))));
#endif

    assert(frame_object->m_type_description == NULL);

    // TODO: Do not call this if there is nothing to do. Instead make all the
    // places handle NULL pointer and recognize that there is nothing to do.
    // assert(type_description != NULL && assert(strlen(type_description)>0));
    if (type_description == NULL) {
        type_description = "";
    }

    frame_object->m_type_description = type_description;

    char const *w = type_description;
    char *t = frame_object->m_locals_storage;

    va_list(ap);
    va_start(ap, type_description);

    while (*w != 0) {
        switch (*w) {
        case NUITKA_TYPE_DESCRIPTION_OBJECT: {
            PyObject *value = va_arg(ap, PyObject *);
            memcpy(t, &value, sizeof(PyObject *));
            Py_XINCREF(value);
            t += sizeof(PyObject *);

            break;
        }
        case NUITKA_TYPE_DESCRIPTION_OBJECT_PTR: {
            /* Note: We store the pointed object only, so this is only
               a shortcut for the calling side. */
            PyObject **value = va_arg(ap, PyObject **);
            CHECK_OBJECT_X(*value);

            memcpy(t, value, sizeof(PyObject *));

            Py_XINCREF(*value);
            t += sizeof(PyObject *);

            break;
        }
        case NUITKA_TYPE_DESCRIPTION_CELL: {
            struct Nuitka_CellObject *value = va_arg(ap, struct Nuitka_CellObject *);
            assert(Nuitka_Cell_Check((PyObject *)value));
            CHECK_OBJECT(value);
            CHECK_OBJECT_X(value->ob_ref);

            memcpy(t, &value, sizeof(struct Nuitka_CellObject *));
            Py_INCREF(value);

            t += sizeof(struct Nuitka_CellObject *);

            break;
        }
        case NUITKA_TYPE_DESCRIPTION_NULL: {
            NUITKA_MAY_BE_UNUSED void *value = va_arg(ap, struct Nuitka_CellObject *);

            break;
        }
        case NUITKA_TYPE_DESCRIPTION_BOOL: {
            int value = va_arg(ap, int);
            memcpy(t, &value, sizeof(int));

            t += sizeof(value);

            break;
        }
        default:
            assert(false);
        }

        w += 1;
    }

    va_end(ap);

    assert(t - frame_object->m_locals_storage <= Nuitka_Frame_GetSize(frame_object));
}

// Make a dump of the active frame stack. For debugging purposes only.
#if _DEBUG_FRAME
void dumpFrameStack(void) {
    PyThreadState *tstate = PyThreadState_GET();

    PyObject *saved_exception_type, *saved_exception_value;
    PyTracebackObject *saved_exception_tb;

    FETCH_ERROR_OCCURRED(&saved_exception_type, &saved_exception_value, &saved_exception_tb);

    int total = 0;

#if PYTHON_VERSION < 0x3b0
    PyFrameObject *current = PyThreadState_GET()->frame;
    while (current != NULL) {
        total++;
        current = current->f_back;
    }

    current = tstate->frame;
#else
    _PyCFrame *current = tstate->cframe;
    while (current != NULL) {
        total++;
        current = current->previous;
    }

    current = tstate->cframe;
#endif

    PRINT_STRING(">--------->\n");

    while (current) {
#if PYTHON_VERSION < 0x3b0
        PyObject *current_repr = PyObject_Str((PyObject *)current);
        PyObject *code_repr = PyObject_Str((PyObject *)current->f_code);
#else
        PyObject *current_repr = NULL;
        if (current->current_frame->frame_obj != NULL) {
            current_repr = PyObject_Str((PyObject *)current->current_frame->frame_obj);
        } else {
            current_repr = const_str_empty;
            Py_INCREF(const_str_empty);
        }
        PyObject *code_repr = PyObject_Str((PyObject *)current->current_frame->f_code);
#endif

        PRINT_FORMAT("Frame stack %d: %s %d %s\n", total--, Nuitka_String_AsString(current_repr), Py_REFCNT(current),
                     Nuitka_String_AsString(code_repr));

        Py_DECREF(current_repr);
        Py_DECREF(code_repr);

#if PYTHON_VERSION < 0x3b0
        current = current->f_back;
#else
        current = current->previous;
#endif
    }

    PRINT_STRING(">---------<\n");

    RESTORE_ERROR_OCCURRED(tstate, saved_exception_type, saved_exception_value, saved_exception_tb);
}

static void PRINT_UNCOMPILED_FRAME(char const *prefix, PyFrameObject *frame) {
    PRINT_STRING(prefix);
    PRINT_STRING(" ");

    if (frame) {
        PyObject *frame_str = PyObject_Str((PyObject *)frame);
        PRINT_ITEM(frame_str);
        Py_DECREF(frame_str);

        PyObject *code_object_str = PyObject_Repr((PyObject *)Nuitka_Frame_GetCodeObject(frame));
        PRINT_ITEM(code_object_str);
        Py_DECREF(code_object_str);

        PRINT_REFCOUNT((PyObject *)frame);
    } else {
        PRINT_STRING("<NULL> no frame");
    }

    PRINT_NEW_LINE();
}

void PRINT_COMPILED_FRAME(char const *prefix, struct Nuitka_FrameObject *frame) {
    return PRINT_UNCOMPILED_FRAME(prefix, &frame->m_frame);
}

void PRINT_INTERPRETER_FRAME(char const *prefix, Nuitka_ThreadStateFrameType *frame) {
#if PYTHON_VERSION < 0x3b0
    PRINT_UNCOMPILED_FRAME(prefix, frame);
#else
    PRINT_STRING(prefix);
    PRINT_STRING(" ");

    if (frame) {
        PRINT_FORMAT("0x%lx ", frame);

        PyObject *code_object_str = PyObject_Repr((PyObject *)frame->f_code);
        PRINT_ITEM(code_object_str);
        Py_DECREF(code_object_str);
    } else {
        PRINT_STRING("<NULL> no frame");
    }

    PRINT_NEW_LINE();
#endif
}

void PRINT_TOP_FRAME(char const *prefix) {
    PyThreadState *tstate = PyThreadState_GET();

#if PYTHON_VERSION < 0x3b0
    PRINT_UNCOMPILED_FRAME(prefix, tstate->frame);
#else
    PRINT_INTERPRETER_FRAME(prefix, tstate->cframe->current_frame);
#endif
}

#endif