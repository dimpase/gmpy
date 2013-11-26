/* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
 * gmpy2_add.c                                                              *
 * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
 * Python interface to the GMP or MPIR, MPFR, and MPC multiple precision   *
 * libraries.                                                              *
 *                                                                         *
 * Copyright 2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007,               *
 *           2008, 2009 Alex Martelli                                      *
 *                                                                         *
 * Copyright 2008, 2009, 2010, 2011, 2012, 2013 Case Van Horsen            *
 *                                                                         *
 * This file is part of GMPY2.                                             *
 *                                                                         *
 * GMPY2 is free software: you can redistribute it and/or modify it under  *
 * the terms of the GNU Lesser General Public License as published by the  *
 * Free Software Foundation, either version 3 of the License, or (at your  *
 * option) any later version.                                              *
 *                                                                         *
 * GMPY2 is distributed in the hope that it will be useful, but WITHOUT    *
 * ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or   *
 * FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public    *
 * License for more details.                                               *
 *                                                                         *
 * You should have received a copy of the GNU Lesser General Public        *
 * License along with GMPY2; if not, see <http://www.gnu.org/licenses/>    *
 * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * */

/* This file implements the + operator, gmpy2.add(), and context.add().
 *
 * Public API
 * ==========
 * The following function is available as part of GMPY2's C API. A NULL
 * value for context implies the function should use the currently active
 * context.
 *
 *   GMPy_Number_Add(Number, Number, context|NULL)
 *
 * Private API
 * ===========
 *   GMPy_mpz_add_fast; called by + via the mpz.nb_add
 *   GMPy_mpq_add_fast; called by + via the mpq.nb_add
 *   GMPy_mpfr_add_fast; called by + via the mpfr.nb_add
 *   GMPy_mpc_add_fast; called by + via the mpc.nb_add
 *
 *   GMPy_Integer_Add(Integer, Integer, context|NULL)
 *   GMPy_Rational_Add(Rational, Rational, context|NULL)
 *   GMPy_Real_Add(Real, Real, context|NULL)
 *   GMPy_Complex_Add(Complex, Complex, context|NULL)
 *
 *   GMPy_Context_Add(context, args)
 *
 */

/* Add two Integer objects (see gmpy2_convert.h). If an error occurs, NULL
 * is returned and an exception is set. If either x or y can't be converted
 * into an mpz, Py_NotImplemented is returned. */

static PyObject *
GMPy_Integer_Add(PyObject *x, PyObject *y, CTXT_Object *context)
{
    MPZ_Object *result;
    mpz_t tempz;
    mpir_si temp_si;
    int overflow;

    if (!(result = GMPy_MPZ_New(context)))
        return NULL;

    if (CHECK_MPZANY(x)) {
        if (PyIntOrLong_Check(y)) {
            temp_si = PyLong_AsSIAndOverflow(y, &overflow);
            if (overflow) {
                mpz_inoc(tempz);
                mpz_set_PyIntOrLong(tempz, y);
                mpz_add(result->z, MPZ(x), tempz);
                mpz_cloc(tempz);
            }
            else if (temp_si >= 0) {
                mpz_add_ui(result->z, MPZ(x), temp_si);
            }
            else {
                mpz_sub_ui(result->z, MPZ(x), -temp_si);
            }
            return (PyObject*)result;
        }

        if (CHECK_MPZANY(y)) {
            mpz_add(result->z, MPZ(x), MPZ(y));
            return (PyObject*)result;
        }
    }

    if (CHECK_MPZANY(y)) {
        if (PyIntOrLong_Check(x)) {
            temp_si = PyLong_AsSIAndOverflow(x, &overflow);
            if (overflow) {
                mpz_inoc(tempz);
                mpz_set_PyIntOrLong(tempz, x);
                mpz_add(result->z, MPZ(y), tempz);
                mpz_cloc(tempz);
            }
            else if (temp_si > 0) {
                mpz_add_ui(result->z, MPZ(y), temp_si);
            }
            else {
                mpz_sub_ui(result->z, MPZ(y), -temp_si);
            }
            return (PyObject*)result;
        }
    }

    if (IS_INTEGER(x) && IS_INTEGER(y)) {
        MPZ_Object *tempx, *tempy;

        tempx = GMPy_MPZ_From_Integer_Temp(x, context);
        tempy = GMPy_MPZ_From_Integer_Temp(y, context);
        if (!tempx || !tempy) {
            Py_XDECREF((PyObject*)tempx);
            Py_XDECREF((PyObject*)tempy);
            Py_DECREF((PyObject*)result);
            return NULL;
        }

        mpz_add(result->z, tempx->z, tempy->z);
        Py_DECREF((PyObject*)tempx);
        Py_DECREF((PyObject*)tempy);
        return (PyObject*)result;
    }

    Py_DECREF((PyObject*)result);
    Py_RETURN_NOTIMPLEMENTED;
}

/* Implement __add__ for MPZ_Object. On entry, one of the two arguments must
 * be an MPZ_Object. If the other object is an Integer, add and return an
 * MPZ_Object. If the other object isn't an MPZ_Object, call the appropriate
 * function. If no appropriate function can be found, return NotImplemented.
 */

static PyObject *
GMPy_mpz_add_fast(PyObject *x, PyObject *y)
{
    if (IS_INTEGER(x) && IS_INTEGER(y))
        return GMPy_Integer_Add(x, y, NULL);

    if (IS_RATIONAL(x) && IS_RATIONAL(y))
        return GMPy_Rational_Add(x, y, NULL);

    if (IS_REAL(x) && IS_REAL(y))
        return GMPy_Real_Add(x, y, NULL);

    if (IS_COMPLEX(x) && IS_COMPLEX(y))
        return GMPy_Complex_Add(x, y, NULL);

    Py_RETURN_NOTIMPLEMENTED;
}

/* Add two Rational objects (see gmpy2_convert.h). Returns None and
 * raises TypeError if both objects are not valid rationals. GMPy_Rational_Add
 * is intended to be called from GMPy_Number_Add(). */

static PyObject *
GMPy_Rational_Add(PyObject *x, PyObject *y, CTXT_Object *context)
{
    MPQ_Object *result;

    if (!(result = GMPy_MPQ_New(context)))
        return NULL;

    if (MPQ_Check(x) && MPQ_Check(y)) {
        mpq_add(result->q, MPQ(x), MPQ(y));
        return (PyObject*)result;
    }

    if (IS_RATIONAL(x) && IS_RATIONAL(y)) {
        MPQ_Object *tempx, *tempy;

        tempx = GMPy_MPQ_From_Number_Temp(x, context);
        tempy = GMPy_MPQ_From_Number_Temp(y, context);
        if (!tempx || !tempy) {
            Py_XDECREF((PyObject*)tempx);
            Py_XDECREF((PyObject*)tempy);
            Py_DECREF((PyObject*)result);
            return NULL;
        }

        mpq_add(result->q, tempx->q, tempy->q);
        Py_DECREF((PyObject*)tempx);
        Py_DECREF((PyObject*)tempy);
        return (PyObject*)result;
    }

    Py_DECREF((PyObject*)result);
    Py_RETURN_NOTIMPLEMENTED;
}

/* Implement __add__ for Pympq. On entry, one of the two arguments must
 * be a Pympq. If the other object is a Rational, add and return a Pympq.
 * If the other object isn't a Pympq, call the appropriate function. If
 * no appropriate function can be found, return NotImplemented. */

static PyObject *
GMPy_mpq_add_fast(PyObject *x, PyObject *y)
{
    CTXT_Object *context = NULL;

    if (IS_RATIONAL(x) && IS_RATIONAL(y))
        return GMPy_Rational_Add(x, y, context);

    if (IS_REAL(x) && IS_REAL(y))
        return GMPy_Real_Add(x, y, context);

    if (IS_COMPLEX(x) && IS_COMPLEX(y))
        return GMPy_Complex_Add(x, y, context);

    Py_RETURN_NOTIMPLEMENTED;
}

/* Addition can be performed by the equivalent of mpfr.__add__ or by
 * gmpy2.add().
 *
 *   GMPy_Real_Add(x, y, context) returns x+y using the provided context. If
 *   provided context is NULL, then the current context is used. If an error
 *   occurs, NULL is returned and an exception is set. If either x or y can't
 *   be converted to an mpfr, then Py_NotImplemented is returned.
*    GMPy_Real_Add() will not try to promote the result to a different type
 *   (i.e. mpc).
 *
 *   GMPy_mpfr_add_fast(x, y) is the entry point for mpfr.__add__.
 */

/* Attempt to add two numbers and return an mpfr. The code path is optimized by
 * checking for mpfr objects first. Returns Py_NotImplemented if both objects
 * are not valid reals.  */

static PyObject *
GMPy_Real_Add(PyObject *x, PyObject *y, CTXT_Object *context)
{
    MPFR_Object *result;

    CHECK_CONTEXT_SET_EXPONENT(context);

    if (!(result = GMPy_MPFR_New(0, context)))
        return NULL;

    /* This only processes mpfr if the exponent is still in-bounds. Need
     * to handle the rare case at the end. */

    if (MPFR_CheckAndExp(x) && MPFR_CheckAndExp(y)) {
        mpfr_clear_flags();
        result->rc = mpfr_add(result->f, MPFR(x), MPFR(y),
                              GET_MPFR_ROUND(context));
        goto done;
    }

    if (MPFR_CheckAndExp(x)) {
        if (PyIntOrLong_Check(y)) {
            mpz_t tempz;
            mpir_si temp_si;
            int overflow;

            temp_si = PyLong_AsSIAndOverflow(y, &overflow);
            if (overflow) {
                mpz_inoc(tempz);
                mpz_set_PyIntOrLong(tempz, y);
                mpfr_clear_flags();
                result->rc = mpfr_add_z(result->f, MPFR(x), tempz,
                                        GET_MPFR_ROUND(context));
                mpz_cloc(tempz);
                goto done;
            }
            else {
                mpfr_clear_flags();
                result->rc = mpfr_add_si(result->f, MPFR(x), temp_si,
                                         GET_MPFR_ROUND(context));
                goto done;
            }
        }

        if (CHECK_MPZANY(y)) {
            mpfr_clear_flags();
            result->rc = mpfr_add_z(result->f, MPFR(x), MPZ(y),
                                    GET_MPFR_ROUND(context));
            goto done;
        }

        if (IS_RATIONAL(y) || IS_DECIMAL(y)) {
            MPQ_Object *tempy;

            if (!(tempy = GMPy_MPQ_From_Number_Temp(y, context))) {
                Py_DECREF(result);
                return NULL;
            }
            mpfr_clear_flags();
            result->rc = mpfr_add_q(result->f, MPFR(x), tempy->q,
                                    GET_MPFR_ROUND(context));
            Py_DECREF((PyObject*)tempy);
            goto done;
        }

        if (PyFloat_Check(y)) {
            mpfr_clear_flags();
            result->rc = mpfr_add_d(result->f, MPFR(x), PyFloat_AS_DOUBLE(y),
                                    GET_MPFR_ROUND(context));
            goto done;
        }
    }

    if (MPFR_CheckAndExp(y)) {
        if (PyIntOrLong_Check(x)) {
            mpz_t tempz;
            mpir_si temp_si;
            int overflow;

            temp_si = PyLong_AsSIAndOverflow(x, &overflow);
            if (overflow) {
                mpz_inoc(tempz);
                mpz_set_PyIntOrLong(tempz, x);
                mpfr_clear_flags();
                result->rc = mpfr_add_z(result->f, MPFR(y), tempz,
                                        GET_MPFR_ROUND(context));
                mpz_cloc(tempz);
                goto done;
            }
            else {
                mpfr_clear_flags();
                result->rc = mpfr_add_si(result->f, MPFR(y), temp_si,
                                         GET_MPFR_ROUND(context));
                goto done;
            }
        }

        if (CHECK_MPZANY(x)) {
            mpfr_clear_flags();
            result->rc = mpfr_add_z(result->f, MPFR(y), MPZ(x),
                                    GET_MPFR_ROUND(context));
            goto done;
        }

        if (IS_RATIONAL(x) || IS_DECIMAL(x)) {
            MPQ_Object *tempx;

            if (!(tempx = GMPy_MPQ_From_Number_Temp(x, context))) {
                Py_DECREF(result);
                return NULL;
            }
            mpfr_clear_flags();
            result->rc = mpfr_add_q(result->f, MPFR(y), tempx->q,
                                    GET_MPFR_ROUND(context));
            Py_DECREF((PyObject*)tempx);
            goto done;
        }

        if (PyFloat_Check(x)) {
            mpfr_clear_flags();
            result->rc = mpfr_add_d(result->f, MPFR(y), PyFloat_AS_DOUBLE(x),
                                    GET_MPFR_ROUND(context));
            goto done;
        }
    }

    /* In addition to handling PyFloat + PyFloat, the rare case when the
     * exponent bounds have been changed is handled here.
     */

    if (IS_REAL(x) && IS_REAL(y)) {
        MPFR_Object *tempx, *tempy;

        tempx = GMPy_MPFR_From_Real_Temp(x, 0, context);
        tempy = GMPy_MPFR_From_Real_Temp(y, 0, context);
        if (!tempx || !tempy) {
            Py_XDECREF((PyObject*)tempx);
            Py_XDECREF((PyObject*)tempy);
            Py_DECREF(result);
            return NULL;
        }
        mpfr_clear_flags();
        result->rc = mpfr_add(result->f, MPFR(tempx), MPFR(tempy),
                              GET_MPFR_ROUND(context));
        Py_DECREF((PyObject*)tempx);
        Py_DECREF((PyObject*)tempy);
        goto done;
    }

    Py_DECREF((PyObject*)result);
    Py_RETURN_NOTIMPLEMENTED;

  done:
    MPFR_CLEANUP_2(result, context, "addition");
    return (PyObject*)result;
}

/* Implement __add__ for Pympfr. On entry, one of the two arguments must
 * be a Pympfr. If the other object is a Real, add and return a Pympfr.
 * If the other object isn't a Pympfr, call the appropriate function. If
 * no appropriate function can be found, return NotImplemented. */

static PyObject *
GMPy_mpfr_add_fast(PyObject *x, PyObject *y)
{
    CTXT_Object *context = NULL;

    if (IS_REAL(x) && IS_REAL(y))
        return GMPy_Real_Add(x, y, context);

    if (IS_COMPLEX(x) && IS_COMPLEX(y))
        return GMPy_Complex_Add(x, y, context);

    Py_RETURN_NOTIMPLEMENTED;
}

/* GMPy_Complex_Add(x, y, context) returns x+y using the provided context. If
 * context is NULL, then the current context is used. If an error occurs, NULL
 * is returned and an exception is set. If either x or y can't be converted to
 * an mpc, then Py_NotImplemented is returned. */

static PyObject *
GMPy_Complex_Add(PyObject *x, PyObject *y, CTXT_Object *context)
{
    MPC_Object *result;
    CHECK_CONTEXT_SET_EXPONENT(context);

    if (!(result = GMPy_MPC_New(0, 0, context)))
        return NULL;

    if (MPC_CheckAndExp(x) && MPC_CheckAndExp(y)) {
        result->rc = mpc_add(result->c, MPC(x), MPC(y),
                             GET_MPC_ROUND(context));
        goto done;
    }

    if (IS_COMPLEX(x) && IS_COMPLEX(y)) {
        MPC_Object *tempx, *tempy;

        tempx = GMPy_MPC_From_Complex_Temp(x, 0, 0, context);
        tempy = GMPy_MPC_From_Complex_Temp(y, 0, 0, context);
        if (!tempx || !tempy) {
            Py_XDECREF((PyObject*)tempx);
            Py_XDECREF((PyObject*)tempy);
            Py_DECREF((PyObject*)result);
            return NULL;
        }
        result->rc = mpc_add(result->c, tempx->c, tempy->c, GET_MPC_ROUND(context));
        Py_DECREF((PyObject*)tempx);
        Py_DECREF((PyObject*)tempy);
        goto done;
    }

    Py_DECREF((PyObject*)result);
    Py_RETURN_NOTIMPLEMENTED;

  done:
    MPC_CLEANUP_2(result, context, "addition");
    return (PyObject*)result;
}

/* Pympc_add_fast() is called by mpc.__add__. It just gets a borrowed reference
 * to the current context and call Pympc_Add_Complex(). Since mpc is the last
 * step of the numeric ladder, the NotImplemented return value from
 * Pympc_Add_Complex() is correct and is just passed on. */

static PyObject *
GMPy_mpc_add_fast(PyObject *x, PyObject *y)
{
    CTXT_Object *context = NULL;

    return GMPy_Complex_Add(x, y, context);
}

static PyObject *
GMPy_Number_Add(PyObject *x, PyObject *y, CTXT_Object *context)
{
    if (IS_INTEGER(x) && IS_INTEGER(y))
        return GMPy_Integer_Add(x, y, context);

    if (IS_RATIONAL(x) && IS_RATIONAL(y))
        return GMPy_Rational_Add(x, y, context);

    if (IS_REAL(x) && IS_REAL(y))
        return GMPy_Real_Add(x, y, context);

    if (IS_COMPLEX(x) && IS_COMPLEX(y))
        return GMPy_Complex_Add(x, y, context);

    TYPE_ERROR("add(): argument type not supported");
    return NULL;
}

/* Implement context.add() and gmpy2.add(). */

PyDoc_STRVAR(GMPy_doc_add,
"add(x, y) -> number\n\n"
"Return x + y.");

PyDoc_STRVAR(GMPy_doc_context_add,
"context.add(x, y) -> number\n\n"
"Return x + y.");

static PyObject *
GMPy_Context_Add(PyObject *self, PyObject *args)
{
    PyObject *result;
    CTXT_Object *context = NULL;

    if (PyTuple_GET_SIZE(args) != 2) {
        TYPE_ERROR("add(): requires 2 arguments.");
        return NULL;
    }

    if (self && CTXT_Check(self)) {
        /* If we are passed a read-only context, make a copy of it before
         * proceeding. Remember to decref context when we're done. */

        if (((CTXT_Object*)self)->ctx.readonly) {
            context = (CTXT_Object*)GMPy_CTXT_Copy(self, NULL);
            if (!context)
                return NULL;
        }
        else {
            context = (CTXT_Object*)self;
            Py_INCREF((PyObject*)context);
        }
        SET_EXPONENT(context);
    }
    else {
        CHECK_CONTEXT_SET_EXPONENT(context);
        Py_INCREF((PyObject*)context);
    }

    result = GMPy_Number_Add(PyTuple_GET_ITEM(args, 0),
                             PyTuple_GET_ITEM(args, 1),
                             context);
    Py_DECREF((PyObject*)context);
    return result;
}
