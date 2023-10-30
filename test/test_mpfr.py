import math
import sys
from decimal import Decimal
from fractions import Fraction

import pytest
from hypothesis import example, given, settings
from hypothesis.strategies import floats
from supportclasses import a, b, c, d, q, r, z

import gmpy2
from gmpy2 import (cmp, cmp_abs, from_binary, gamma_inc, is_nan, mpc, mpfr,
                   mpfr_grandom, mpfr_nrandom, mpq, mpz, nan, random_state,
                   to_binary, xmpz, zero)


def test_mpfr_gamma_inc():
    assert gamma_inc(1, 1) == mpfr('0.36787944117144233')
    assert gamma_inc(1, 0) == mpfr('1.0')
    assert gamma_inc(0, 1) == mpfr('0.21938393439552029')


def test_mpfr_cmp():
    assert cmp(mpfr(0), mpfr(0)) == 0
    assert cmp(mpfr(0), mpz(0)) == 0
    assert cmp(mpfr(0), mpq(0,1)) == 0
    assert cmp(zero(-1), zero(-1)) == 0
    assert cmp(zero(1), zero(-1)) == 0
    assert cmp(zero(-1), zero(1)) == 0
    assert cmp(mpfr(1), mpfr(0)) == 1
    assert cmp(mpfr(1), mpz(0)) == 1
    assert cmp(mpfr(1), mpq(0,1)) == 1
    assert cmp(mpfr(-1), mpfr(0)) == -1
    assert cmp(mpfr(-1), mpz(0)) == -1
    assert cmp(mpfr(-1), mpq(0,1)) == -1
    assert cmp(nan(), mpfr(0)) == 0
    assert cmp(nan(), mpz(0)) == 0
    assert cmp(nan(), mpq(0,1)) == 0

    gmpy2.get_context().clear_flags()

    assert cmp(nan(), 1) == 0
    assert gmpy2.get_context().erange is True

    assert cmp_abs(mpfr(-1), mpfr(0)) == 1
    assert cmp_abs(mpfr(-1), mpz(0)) == 1
    assert cmp_abs(mpfr(-1), mpq(0,1)) == 1
    assert cmp_abs(mpfr(0), mpfr(-1)) == -1
    assert cmp_abs(mpz(0), mpfr(-1)) == -1
    assert cmp_abs(mpq(0,1), mpfr(-1)) == -1

    assert cmp(mpfr(1.5), q) == 0
    assert cmp(r, mpfr(1.5)) == 0


def test_mpfr_comparisons():
    from supportclasses import a, r, q

    assert mpfr(1.5) == q
    assert r == mpfr(1.5)
    assert (r == a) is False

    a = mpz(123)
    r = mpfr('inf')
    q = mpq('45/7')
    f = float(0.7)
    r2 = mpfr(454.6)

    assert (r == a, r != a, r > a, r >= a, r < a, r <= a) == (False, True, True, True, False, False)

    r = mpfr('-inf')

    assert (r == a, r != a, r > a, r >= a, r < a, r <= a) == (False, True, False, False, True, True)

    r = mpfr('nan')

    assert (r == a, r != a, r > a, r >= a, r < a, r <= a) == (False, True, False, False, False, False)
    assert (r == q, r != q, r > q, r >= q, r < q, r <= q) == (False, True, False, False, False, False)
    assert (r == f, r != f, r > f, r >= f, r < f, r <= f) == (False, True, False, False, False, False)
    assert (r == r2, r != r2, r > r2, r >= r2, r < r2, r <= r2) == (False, True, False, False, False, False)

    r = mpfr(126.5)

    assert (r == a, r != a, r > a, r >= a, r < a, r <= a) == (False, True, True, True, False, False)
    assert (r == q, r != q, r > q, r >= q, r < q, r <= q) == (False, True, True, True, False, False)

    f = float(126.5)

    assert (r == f, r != f, r > f, r >= f, r < f, r <= f) == (True, False, False, True, False, True)
    assert (r == r2, r != r2, r > r2, r >= r2, r < r2, r <= r2) == (False, True, False, False, True, True)


def test_mpfr_conversion():
    x = mpfr(a)
    assert isinstance(x, mpfr)
    assert x == 1.5
    pytest.raises(TypeError, lambda: mpfr(b))
    pytest.raises(TypeError, lambda: mpfr(c))
    pytest.raises(TypeError, lambda: mpfr(d))

    pytest.raises(OverflowError, lambda: mpz(mpfr('inf')))

    assert mpz(mpfr(5.51)) == mpz(6)

    pytest.raises(OverflowError, lambda: xmpz(mpfr('inf')))

    assert xmpz(mpfr(5.51)) == xmpz(6)

    pytest.raises(OverflowError, lambda: mpq(mpfr('inf')))

    assert mpq(mpfr(4.5)) == mpq(9,2)
    assert mpq(mpfr(0)) == mpq(0,1)
    assert int(mpfr(5.3)) == 5
    assert float(mpfr(5.3)) == 5.3
    assert str(float('5.656')) == '5.656'


def test_mpfr_create():
    assert mpfr() == mpfr('0.0')
    assert mpfr(0) == mpfr('0.0')
    assert mpfr(1) == mpfr('1.0')
    assert mpfr(-1) == mpfr('-1.0')
    assert mpfr("123e17") == mpfr('1.23e+19')

    pytest.raises(ValueError, lambda: mpfr("foo"))

    assert mpfr(1,100) == mpfr('1.0',100)
    assert mpfr("1",100) == mpfr('1.0',100)

    pytest.raises(TypeError, lambda: mpfr("1","hi"))

    assert mpfr("-inf") == mpfr('-inf')
    assert mpfr("inf") == mpfr('inf')
    assert is_nan(mpfr("nan"))
    assert mpfr(float("-inf")) == mpfr('-inf')
    assert mpfr(float("inf")) == mpfr('inf')
    assert is_nan(mpfr(float("nan")))
    assert mpfr(float("0")) == mpfr('0.0')
    assert mpfr(float("-0")) == mpfr('-0.0')
    assert mpfr("-0") == mpfr('-0.0')

    a = float("1.2345678901234567890")
    b = mpfr("1.2345678901234567890")
    assert a == 1.2345678901234567
    assert b == mpfr('1.2345678901234567')
    assert a == b

    c = mpfr(b)

    assert b is c
    assert mpfr(Fraction(0,1)) == mpfr('0.0')
    assert mpfr(Fraction(0,-1)) == mpfr('0.0')
    assert mpfr(Fraction(1,2)) == mpfr('0.5')
    assert mpfr(-1) == mpfr('-1.0')
    assert mpfr(12345678901234567890) == mpfr('1.2345678901234567e+19')
    assert mpfr(mpz(12345678901234567890)) == mpfr('1.2345678901234567e+19')
    assert mpfr(mpz(-1)) == mpfr('-1.0')
    assert mpfr(2**15 - 1) == mpfr('32767.0')
    assert mpfr(2**15) == mpfr('32768.0')
    assert mpfr(2**15 + 1) == mpfr('32769.0')
    assert mpfr(2**30 - 1) == mpfr('1073741823.0')
    assert mpfr(2**30 ) == mpfr('1073741824.0')
    assert mpfr(2**30 + 1) == mpfr('1073741825.0')

    ctx = gmpy2.get_context()
    ctx.clear_flags()
    a = mpfr("1.2")

    assert a.rc == -1

    ctx.clear_flags()
    a = mpfr("1.25")

    assert a.rc == 0

    ctx.clear_flags()
    a = mpfr('nan')

    assert is_nan(a)
    assert ctx.invalid

    ctx.clear_flags()

    assert is_nan(mpfr(a))
    assert not ctx.invalid

    ctx.clear_flags()

    assert is_nan(mpfr(float('nan')))
    assert ctx.invalid

    gmpy2.set_context(gmpy2.ieee(128))

    assert mpfr(1)/7 == mpfr('0.14285714285714285714285714285714285',113)
    assert mpfr(1.0/7) == mpfr('0.142857142857142849212692681248881854',113)
    assert mpfr(1.0/7).digits(2) == ('10010010010010010010010010010010010010010010010010010000000000000000000000000000000000000000000000000000000000000', -2, 113)

    gmpy2.set_context(gmpy2.ieee(32))

    assert mpfr(1)/7 == mpfr('0.142857149',24)
    assert (mpfr(1)/7).digits(2) == ('100100100100100100100101', -2, 24)
    assert mpfr(1.0/7) == mpfr('0.142857149',24)
    assert mpfr(1.0/7).digits(2) == ('100100100100100100100101', -2, 24)
    assert mpfr(1.0/7, precision=0) == mpfr('0.142857149',24)
    assert repr(mpfr(1.0/7, precision=1)) == "mpfr('0.14285714285714285')"


@settings(max_examples=1000)
@given(floats())
@example(0.0)
@example(1.0)
@example(2.0)
@example(-1.0)
@example(123.456)
@example(123.5)
@example(float('inf'))
@example(-float('inf'))
@example(float('nan'))
def test_mpfr_hash(x):
    if math.isnan(x):
        if sys.version_info < (3, 10):
            assert hash(mpfr(x)) == hash(x) == sys.hash_info.nan
        else:
            assert hash(mpfr(x)) != hash(x)
    else:
        assert hash(mpfr(x)) == hash(x)


@given(floats())
@example(0.0)
@example(1.0)
@example(-1.0)
@example(+float('inf'))
@example(-float('inf'))
@example(float('nan'))
@example(1.345)
def test_mpfr_to_from_binary_bulk(r):
    x = mpfr(r)
    y = from_binary(to_binary(x))
    assert x == y or (is_nan(x) and is_nan(y))


def test_mpfr_to_from_binary():
    x = mpfr("1.345e1000")
    assert x==from_binary(to_binary(x))
    x = gmpy2.const_pi()
    assert x.rc == -1
    y = from_binary(to_binary(x))
    assert x == y and y.rc == -1
    -1
    with gmpy2.local_context() as ctx:
        ctx.precision = 100
        x = gmpy2.const_pi()
        assert x == from_binary(to_binary(x))
        ctx.precision = 200
        x = mpfr(gmpy2.const_pi())
        assert x == from_binary(to_binary(x))
        x = gmpy2.const_pi()
        ctx.precision = 300
        x = from_binary(to_binary(x))
        assert x.precision == 200


def test_mpfr_random():
    assert gmpy2.mpfr_random(random_state(42)) == mpfr('0.93002690534702315')


def test_mpfr_grandom():
    assert mpfr_grandom(random_state(42)) == (mpfr('-0.32898912492644183'),
                                              mpfr('0.03656576719642516'))


def test_mpfr_nrandom():
    assert mpfr_nrandom(random_state(42)) == mpfr('-0.32898912492644183')


def test_mpfr_mpmath():
    mpmath = pytest.importorskip("mpmath")
    a, b, c, d = '1.1', '-1.1', '-3.14', '0'
    assert mpfr(a)._mpf_ == (0, mpz(4953959590107546), -52, 53)
    assert mpmath.mpf(mpfr(a)) == mpmath.mpf(a)
    assert mpfr(b)._mpf_ == (1, mpz(4953959590107546), -52, 53)
    assert mpmath.mpf(mpfr(b)) == mpmath.mpf(b)
    assert mpfr(c, precision=10)._mpf_ == (1, mpz(804), -8, 10)
    assert mpmath.mpf(mpfr(c, precision=10), prec=10) == mpmath.mpf(c, prec=10)
    assert mpfr(d)._mpf_ == (0, mpz(0), 1, 1)


def test_mpfr_format():
    r, r1, r2 = mpfr(5.6), mpfr(-3), mpfr(5)

    assert '{:<30}'.format(r1) == '-3.000000                     '
    assert '{:>+20}'.format(r2) == '           +5.000000'
    assert '{:>-15}'.format(r2) == '       5.000000'
    assert '{:>-15}'.format(r1) == '      -3.000000'
    assert '{:U}'.format(r) == '5.600000'

    pytest.raises(ValueError, lambda: '{:U-}'.format(r))

    assert '{:Z}'.format(r) == '5.599999'

    pytest.raises(ValueError, lambda: '{:Z+}'.format(r))

    assert '{:+Z}'.format(r) == '+5.599999'

    pytest.raises(ValueError, lambda: '{:Z }'.format(r))

    assert '{:.10f}'.format(r) == '5.6000000000'
    assert '{:.10f.}'.format(r) == '5.6000000000'

    pytest.raises(ValueError, lambda: '{:Z.}'.format(r))
    pytest.raises(ValueError, lambda: '{:->}'.format(r))
    pytest.raises(ValueError, lambda: '{:YZ}'.format(r))


def test_mpfr_digits():
    r, r2 = mpfr(5.6), mpfr(5)

    assert r.digits() == ('55999999999999996', 1, 53)
    assert r.digits(2) == ('10110011001100110011001100110011001100110011001100110', 3, 53)
    assert r.digits(2,54) == ('101100110011001100110011001100110011001100110011001100', 3, 53)
    assert r.digits(10,54) == ('559999999999999964472863211994990706443786621093750000', 1, 53)
    assert r2.digits(2) == ('10100000000000000000000000000000000000000000000000000', 3, 53)

    pytest.raises(TypeError, lambda: r2.digits(2, 5, 6))
    pytest.raises(ValueError, lambda: r.digits(0))


def test_mpfr_abs():
    a = mpfr(1.0)
    b = abs(a)

    assert a is not b
    assert abs(mpfr(1, precision=100)) == mpfr('1.0')

    ctx = gmpy2.get_context()
    ctx.clear_flags()

    assert is_nan(abs(mpfr('nan')))
    assert ctx.invalid

    ctx.clear_flags()

    assert abs(mpfr('inf')) == mpfr('inf')
    assert abs(mpfr('-inf')) == mpfr('inf')


def test_mpfr_sub():
    assert mpfr(10) - 1 == mpfr('9.0')
    assert 10 - mpfr(1) == mpfr('9.0')
    assert mpfr(10) - mpz(1) == mpfr('9.0')
    assert mpz(10) - mpfr(1) == mpfr('9.0')
    assert mpfr(10) - mpfr(1) == mpfr('9.0')
    assert mpfr(10) - mpq(1,1) == mpfr('9.0')
    assert mpq(10,1) - mpfr(1) == mpfr('9.0')
    assert mpfr(10) - Fraction(1,1) == mpfr('9.0')
    assert Fraction(10,1) - mpfr(1) == mpfr('9.0')
    assert mpfr(10) - 1.0 == mpfr('9.0')
    assert 10.0 - mpfr(1) == mpfr('9.0')
    assert mpfr(0) - (1 << 100) == mpfr('-1p100', base=2)
    assert (1 << 100) - mpfr(0) == mpfr('1p100', base=2)
    assert mpfr(10) - z == mpfr('8.0')
    assert mpfr(10) - q == mpfr('8.5')
    assert mpfr(10) - r == mpfr('8.5')


def test_mpfr_mul():
    c = 12345678901234567890

    assert mpfr(10) * 1 == mpfr('10.0')
    assert 10 * mpfr(1) == mpfr('10.0')
    assert mpfr(10) * mpz(1) == mpfr('10.0')
    assert mpz(10) * mpfr(1) == mpfr('10.0')
    assert mpfr(10) * mpfr(1) == mpfr('10.0')
    assert mpfr(10) * mpq(1,1) == mpfr('10.0')
    assert mpq(10,1) * mpfr(1) == mpfr('10.0')
    assert mpfr(10) * Fraction(1,1) == mpfr('10.0')
    assert Fraction(10,1) * mpfr(1) == mpfr('10.0')
    assert mpfr(10) * 1.0 == mpfr('10.0')
    assert 10.0 * mpfr(1) == mpfr('10.0')
    assert mpfr(1) * c == mpfr(c)
    assert c * mpfr(1) == mpfr(c)
    assert mpfr(10) * z == mpfr('20.0')
    assert mpfr(10) * q == mpfr('15.0')
    assert mpfr(10) * r == mpfr('15.0')

    pytest.raises(TypeError, lambda: mpfr(10) * 'a')
    pytest.raises(TypeError, lambda: 'a' * mpfr(10))


def test_mpfr_divmod():
    pytest.raises(TypeError, lambda: divmod(mpfr(1),'a'))

    ctx = gmpy2.context()

    assert ctx.divmod(mpfr(2),mpfr(1)) == (mpfr('2.0'), mpfr('0.0'))

    pytest.raises(TypeError, lambda: divmod(mpfr(1), mpc(1,2)))

    assert divmod(mpfr(1.2), mpfr(0.7)) == (mpfr('1.0'), mpfr('0.5'))

    ctx = gmpy2.ieee(64)
    gmpy2.set_context(ctx)

    assert divmod(mpfr(1.2), mpfr(0.7)) == (mpfr('1.0'), mpfr('0.5'))
    ctx.clear_flags()

    assert ctx.divzero is False
    assert all(map(ctx.is_nan, divmod(mpfr(1.2), mpfr(0))))

    with gmpy2.local_context(trap_divzero=True):
        pytest.raises(gmpy2.DivisionByZeroError, lambda: divmod(mpfr(1), mpfr(0)))
    with gmpy2.local_context(trap_invalid=True):
        pytest.raises(gmpy2.InvalidOperationError, lambda: divmod(gmpy2.nan(), mpfr(1)))
    with gmpy2.local_context(trap_invalid=True):
        pytest.raises(gmpy2.InvalidOperationError, lambda: divmod(mpfr(1), gmpy2.inf()))

    assert divmod(mpfr(111), mpfr(-222)) == (mpfr('-1.0'), mpfr('-111.0'))


def test_mpfr_mod():
    r = mpfr('0.0') % mpfr('-1.0')
    assert r.is_zero() and r.is_signed()


def test_mpfr_pow():
    r1, r2 = mpfr(5.0), mpfr(2.5)
    ctx = gmpy2.get_context()

    assert r1 ** mpz(2) == mpfr('25.0')
    assert r2 ** mpz(2) == mpfr('6.25')
    assert r2 ** 2 == mpfr('6.25')
    assert pow(r1, r2) == mpfr('55.901699437494742')
    assert ctx.pow(r1, r2) == mpfr('55.901699437494742')
    assert ctx.pow(r1, r2) == r1 ** r2

    pytest.raises(TypeError, lambda: pow(r1, r2, 5))
    pytest.raises(TypeError, lambda: ctx.pow(r1, r2, 5))

    assert pow(r1, 4) == mpfr('625.0')
    assert ctx.pow(r1, 4) == mpfr('625.0')


def test_mpfr_subnormalize():
    gmpy2.set_context(gmpy2.ieee(64))

    zeroes = '0.' + '0' * 323

    assert mpfr(zeroes + '2470328229206232720') == mpfr('0.0')
    assert mpfr(zeroes + '2470328229206232721') == mpfr('4.9406564584124654e-324')
    assert mpfr(zeroes + '247032822920623272088') == mpfr('0.0')
    assert mpfr(zeroes + '247032822920623272089') == mpfr('4.9406564584124654e-324')

    gmpy2.set_context(gmpy2.ieee(32))

    def fmt(v):
        return '{:.23b}'.format(v)


    a = mpfr('0x1p-126')

    assert fmt(a) == '1.00000000000000000000000p-126'
    assert fmt(gmpy2.next_below(a)) == '1.11111111111111111111110p-127'
    assert fmt(gmpy2.next_above(a)) == '1.00000000000000000000001p-126'
    assert fmt(gmpy2.next_below(0)) == '-1.00000000000000000000000p-149'
    assert fmt(gmpy2.next_above(0)) == '1.00000000000000000000000p-149'
    assert fmt(gmpy2.next_toward(a, -10)) == '1.11111111111111111111110p-127'
    assert fmt(gmpy2.next_toward(a, 10)) == '1.00000000000000000000001p-126'

    gmpy2.set_context(gmpy2.context())


def test_mpfr_as_integer_ratio():
    assert mpfr('1.1e+2').as_integer_ratio() == (mpz(110), mpz(1))


def test_mpfr_round():
    pytest.raises(TypeError, lambda: round(mpfr('1.0'), "spam"))

    r = round(mpfr('-0.0'), 123)
    assert r.is_zero() and r.is_signed()

    assert round(mpfr('12.34'), -1) == mpfr('10.0')
