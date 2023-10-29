from fractions import Fraction

import pytest
from hypothesis import example, given, settings
from hypothesis.strategies import complex_numbers
from supportclasses import a, b, c, cx, d, q, r, z

import gmpy2
from gmpy2 import (cmp, cmp_abs, from_binary, get_context, is_nan, mpc,
                   mpc_random, mpfr, mpq, mpz, nan, random_state, to_binary)


def test_mpc_cmp():
    pytest.raises(TypeError, lambda: cmp(mpc(1,2), mpc(3,4)))
    assert cmp_abs(mpc(1,2), mpc(3,4)) == -1
    assert cmp_abs(mpc(1,2), mpc(1,2)) == 0
    assert cmp_abs(mpc(3,4), mpc(1,2)) == 1
    gmpy2.get_context().clear_flags()
    assert gmpy2.get_context().erange is False
    assert cmp_abs(mpc(nan(),1), mpc(4.5)) == 0
    assert gmpy2.get_context().erange is True


def test_mpc_conversion():
    x = mpc(a)
    assert isinstance(x, mpc)
    assert x == 42+67j

    pytest.raises(TypeError, lambda: mpc(b))
    pytest.raises(TypeError, lambda: mpc(c))
    pytest.raises(TypeError, lambda: mpc(d))

    assert mpc(mpfr(5.6), precision=(0,0)) == mpc('5.5999999999999996+0.0j')
    assert mpc(Fraction(4,5)) == mpc('0.80000000000000004+0.0j')
    assert mpc(b'5+6j') == mpc('5.0+6.0j')
    assert mpc('5+6j') == mpc('5.0+6.0j')

    pytest.raises(ValueError, lambda: mpc('\xc3'))
    pytest.raises(ValueError, lambda: mpc('notanumber'))
    pytest.raises(ValueError, lambda: mpc('\0'))

    assert mpc('(5+6j)') == mpc('5.0+6.0j')
    assert mpc('   5+6j   ') == mpc('5.0+6.0j')

    pytest.raises(ValueError, lambda: mpc('5+6ji'))

    assert str(mpc(5,6)) == '5.0+6.0j'
    assert complex(mpc(4,5)) == (4+5j)


def test_mpc_creation():
    ctx = gmpy2.get_context()
    ctx.clear_flags()
    a = mpc("1.2")
    assert a.rc == (-1, 0)
    assert ctx.inexact
    ctx.clear_flags()
    a = mpc("(1 2)")
    assert a == 1 + 2j
    assert a.rc == (0, 0)
    assert ctx.inexact is False
    ctx.clear_flags()
    a = mpc("1   + 2.1  j")
    assert a == 1 + 2.1j
    assert a.rc == (0, 1)
    assert ctx.inexact


def test_mpc_random():
    assert (mpc_random(random_state(42))
            == mpc('0.86555158787663011+0.4422082613292212j'))


def test_mpc_to_from_binary():
    x = mpc("0+0j")
    assert x == from_binary(to_binary(x))
    x = mpc("1+0j")
    assert x == from_binary(to_binary(x))
    x = mpc("-1+0j")
    assert x == from_binary(to_binary(x))
    x = mpc("0+1j")
    assert x == from_binary(to_binary(x))
    x = mpc("0-1j")
    assert x == from_binary(to_binary(x))
    x = mpc("inf+0j")
    assert x == from_binary(to_binary(x))
    x = mpc("0+infj")
    assert x == from_binary(to_binary(x))
    x = mpc("inf-infj")
    assert x == from_binary(to_binary(x))
    x = mpc("inf+nanj")
    y = from_binary(to_binary(x))
    assert x.real == y.real
    assert is_nan(y.imag)
    x = mpc("-inf+0j")
    assert x == from_binary(to_binary(x))
    x = mpc("0-infj")
    assert x == from_binary(to_binary(x))
    x = mpc("-inf-infj")
    assert x == from_binary(to_binary(x))
    x = mpc("-inf+nanj")
    y = from_binary(to_binary(x))
    assert x.real == y.real
    assert is_nan(y.imag)
    x = mpc("nan+0j")
    y = from_binary(to_binary(x))
    assert x.imag == y.imag
    assert is_nan(y.real)
    x = mpc("0+nanj")
    y = from_binary(to_binary(x))
    assert x.real == y.real
    assert is_nan(y.imag)
    x = mpc("nan-infj")
    y = from_binary(to_binary(x))
    assert x.imag == y.imag
    assert is_nan(y.real)
    x = mpc("nan+nanj")
    y = from_binary(to_binary(x))
    assert is_nan(y.real)
    assert is_nan(y.imag)
    get_context().real_prec=100
    get_context().imag_prec=110
    assert (from_binary(to_binary(mpc("1.3-4.7j"))) ==
            mpc('1.2999999999999999999999999999994-4.7000000000000000000000000000000025j',
                (100,110)))


def test_mpc_format():
    gmpy2.set_context(gmpy2.context())

    c, c1 = mpc(mpq(1/3), 5), mpc(-1, -2)

    assert '{:>20}'.format(c) == '  0.333333+5.000000j'
    assert '{:<20}'.format(c) == '0.333333+5.000000j  '
    assert '{:^20}'.format(c) == ' 0.333333+5.000000j '

    pytest.raises(ValueError, lambda: '{:<<20}'.format(c))

    assert '{:>+20}'.format(c) == ' +0.333333+5.000000j'

    pytest.raises(ValueError, lambda: '{:+^20}'.format(c))

    assert '{:.10f}'.format(c) == '0.3333333333+5.0000000000j'

    pytest.raises(ValueError, lambda: '{:Z.10f}'.format(c))
    pytest.raises(ValueError, lambda: '{:Z 10}'.format(c))

    assert '{:Z}'.format(c) == '0.333333+5.000000j'
    assert '{:U}'.format(c) == '0.333334+5.000000j'

    pytest.raises(ValueError, lambda: '{:PU}'.format(c))

    assert '{:UP}'.format(c) == '0.333334+5.000000j'

    pytest.raises(ValueError, lambda: '{:PP}'.format(c))

    assert '{:G}'.format(c) == '0.333333+5.0j'
    assert '{:M}'.format(c) == '(0.333333 5.000000)'
    assert '{:b}'.format(c) == '1.0101010101010101010101010101010101010101010101010101p-2+1.01p+2j'
    assert '{:a}'.format(c) == '0x5.5555555555554p-4+0x5p+0j'
    assert '{:e}'.format(c) in ('3.3333333333333331e-01+5e+00j', '3.3333333333333331e-01+5.0000000000000000e+00j')
    assert '{:M}'.format(c1) == '(-1.000000 -2.000000)'


def test_mpc_digits():
    c = mpc(mpq(1/3), 5)

    assert c.digits(8) == (('2525252525252525250', 0, 53), ('5000000000000000000', 1, 53))
    assert c.digits(8, 2) == (('25', 0, 53), ('50', 1, 53))

    pytest.raises(ValueError, lambda: c.digits(8, -2))
    pytest.raises(ValueError, lambda: c.digits(0))


def test_mpc_sub():
    pytest.raises(TypeError, lambda: mpc(1,2) - 'a')

    assert mpfr(1) - mpc(1,2) == mpc('0.0-2.0j')
    assert mpc(1,2) - mpfr(1) == mpc('0.0+2.0j')
    assert mpc(1,2) - 1+0j == mpc('0.0+2.0j')
    assert 1+0j - mpc(1,2) == mpc('0.0-2.0j')
    assert mpc(1,2) - z == mpc('-1.0+2.0j')
    assert mpc(1,2) - q == mpc('-0.5+2.0j')
    assert mpc(1,2) - r == mpc('-0.5+2.0j')
    assert mpc(1,2) - cx == mpc('-41.0-65.0j')


def test_mpc_mul():
    pytest.raises(TypeError, lambda: mpc(1,2) * 'a')

    assert mpfr(1) * mpc(1,2) == mpc('1.0+2.0j')
    assert mpc(1,2) * mpfr(1) == mpc('1.0+2.0j')
    assert mpc(1,2) * mpfr(-1) == mpc('-1.0-2.0j')
    assert mpc(1,2) * (1+0j) == mpc('1.0+2.0j')
    assert (1+0j) * mpc(1,2) == mpc('1.0+2.0j')
    assert mpc(1,2) * z == mpc('2.0+4.0j')
    assert mpc(1,2) * q == mpc('1.5+3.0j')
    assert mpc(1,2) * r == mpc('1.5+3.0j')
    assert mpc(1,2) * cx == mpc('-92.0+151.0j')


def test_mpc_divmod():
    pytest.raises(TypeError, lambda: divmod(mpc(1),'a'))

    ctx = gmpy2.context()

    pytest.raises(TypeError, lambda: ctx.divmod(mpc(1,2),mpc(3,4)))
    pytest.raises(TypeError, lambda: divmod(mpc(1,2), mpc(1,2)))
    pytest.raises(TypeError, lambda: ctx.divmod(mpc(1,2),mpc(3,4)))


def test_mpc_pow():
    c1, c2 = mpc(2,5), mpc(5,2)
    ctx = gmpy2.get_context()

    assert ctx.pow(complex(2,5), complex(5,2)) == mpc('-416.55882051164394+44.334999625388825j')
    assert pow(c1, c2) == mpc('-416.55882051164394+44.334999625388825j')
    assert ctx.pow(c1, c2) == mpc('-416.55882051164394+44.334999625388825j')
    assert ctx.pow(c1, c2) == c1 ** c2

    pytest.raises(TypeError, lambda: pow(c1, c2, 5))

    assert pow(c1, 5) == mpc('4282.0-1475.0j')
    assert c1 ** mpz(5) == mpc('4282.0-1475.0j')
    assert c1 ** mpfr(2.5) == mpc('-66.373652915897722+11.111336616269842j')


@settings(max_examples=1000)
@given(complex_numbers(allow_nan=False))
@example(complex())
@example(complex(-1))
@example(complex(-2))
def test_mpc_hash(c):
    assert hash(mpc(c)) == hash(c)


def test_mpc_exc():
    gmpy2.set_context(gmpy2.ieee(32))

    ctx = gmpy2.get_context()
    ctx.trap_overflow = True
    ctx.trap_underflow = True

    c = mpc(0.1 + 0.1j)

    pytest.raises(gmpy2.UnderflowResultError, lambda: c**201)
    pytest.raises(gmpy2.OverflowResultError, lambda: c**-201)

    ctx.trap_inexact = True

    pytest.raises(gmpy2.InexactResultError, lambda: mpc(0.25)**0.25)

    ctx.trap_invalid = True

    pytest.raises(gmpy2.InvalidOperationError, lambda: mpc(mpfr('nan')))
