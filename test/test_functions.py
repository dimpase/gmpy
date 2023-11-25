from fractions import Fraction

import pytest

import gmpy2
from gmpy2 import (acos, acosh, asin, asinh, atan, atan2, atanh, bincoef,
                   c_div, c_divmod, c_mod, can_round, check_range, comb,
                   context, copy_sign, cos, cosh, cot, coth, csc, csch,
                   degrees, divexact, divm, double_fac, f2q, f_div, f_divmod,
                   f_mod, fac, fib, fib2, fma, fmma, fmms, fms, free_cache,
                   from_binary, gcd, gcdext, get_context, get_emax_max,
                   get_emin_min, get_exp, ieee, inf, invert, iroot, iroot_rem,
                   is_bpsw_prp, is_euler_prp, is_extra_strong_lucas_prp,
                   is_fermat_prp, is_fibonacci_prp, is_finite, is_infinite,
                   is_lucas_prp, is_nan, is_selfridge_prp, is_strong_bpsw_prp,
                   is_strong_lucas_prp, is_strong_prp, is_strong_selfridge_prp,
                   is_zero, isqrt, isqrt_rem, jacobi, kronecker, lcm, legendre,
                   lucas, lucas2, maxnum, minnum, mpc, mpfr,
                   mpfr_from_old_binary, mpq, mpq_from_old_binary, mpz,
                   mpz_from_old_binary, multi_fac, nan, next_prime, norm,
                   phase, polar, powmod, powmod_sec, primorial, proj, radians,
                   rect, remove, root, root_of_unity, rootn, sec, sech,
                   set_context, set_exp, set_sign, sign, sin, sin_cos, sinh,
                   sinh_cosh, t_div, t_divmod, t_mod, tan, tanh, zero)


def test_root():
    assert root(zero(1), 2) == mpfr('0.0')
    assert root(zero(-1), 2) == mpfr('-0.0')
    assert root(zero(-1), 3) == mpfr('-0.0')
    assert root(zero(-1), 4) == mpfr('-0.0')
    assert root(zero(-1), 5) == mpfr('-0.0')
    assert root(zero(-1), 6) == mpfr('-0.0')
    assert root(2, 2) == mpfr('1.4142135623730951')
    assert root(mpz(2), 2) == mpfr('1.4142135623730951')
    assert root(mpq(2), 2) == mpfr('1.4142135623730951')
    assert root(mpfr(2), 2) == mpfr('1.4142135623730951')
    pytest.raises(TypeError, lambda: root(mpc(2), 2))
    assert is_nan(root(-2, 2))
    pytest.raises(OverflowError, lambda: root(2, -2))
    pytest.raises(TypeError, lambda: root(2, 0.5))


def test_rootn():
    assert rootn(zero(1), 2) == mpfr('0.0')
    assert rootn(zero(-1), 2) == mpfr('0.0')
    assert rootn(zero(-1), 3) == mpfr('-0.0')
    assert rootn(zero(-1), 4) == mpfr('0.0')
    assert rootn(zero(-1), 5) == mpfr('-0.0')
    assert rootn(zero(-1), 6) == mpfr('0.0')


def test_maxnum():
    a = mpfr("12.34")
    b = mpfr("45.67")
    nan = mpfr("nan")
    inf = mpfr("inf")

    assert maxnum(a, b) == mpfr('45.670000000000002')
    assert maxnum(b, a) == mpfr('45.670000000000002')
    assert maxnum(a, -b) == mpfr('12.34')
    assert maxnum(a, 123456) == mpfr('123456.0')
    assert maxnum(12345678901234567890, a) == mpfr('1.2345678901234567e+19')
    assert maxnum(0, -1) == mpfr('0.0')
    assert maxnum(1, inf) == mpfr('inf')
    assert maxnum(1, -inf) == mpfr('1.0')
    assert maxnum(nan, a) == mpfr('12.34')
    assert maxnum(a, nan) == mpfr('12.34')
    assert maxnum(nan, inf) == mpfr('inf')
    assert maxnum(nan, -inf) == mpfr('-inf')
    assert is_nan(maxnum(nan, nan))


def test_minnum():
    a = mpfr("12.34")
    b = mpfr("45.67")
    nan = mpfr("nan")
    inf = mpfr("inf")
    minf = mpfr("-inf")

    assert minnum(a, b) == mpfr('12.34')
    assert minnum(b, a) == mpfr('12.34')
    assert minnum(1, inf) == mpfr('1.0')
    assert minnum(minf, a) == mpfr('-inf')
    assert minnum(nan, inf) == mpfr('inf')
    assert is_nan(minnum(nan, nan))


def test_fused():
    assert fma(2,3,4) == mpz(10)
    assert fma(2,3,-4) == mpz(2)
    assert fma(2.0,3,-4) == mpfr('2.0')
    assert fma(2,3.0,-4) == mpfr('2.0')
    assert fma(2,3,-4.0) == mpfr('2.0')
    assert fma(2,mpfr(3),-4.0) == mpfr('2.0')
    assert fma(mpc(2),mpfr(3),-4.0) == mpc('2.0+0.0j')
    assert fms(2,3,4) == mpz(2)
    assert fms(2,3,-4) == mpz(10)

    assert ieee(128).fma(7,1/7,-1) == mpfr('-5.55111512312578270211815834045410156e-17',113)
    assert ieee(128).fma(7,mpq(1,7),-1) == mpq(0,1)

    pytest.raises(TypeError, lambda: fma(1,2,"r"))

    assert fma(1,2,mpq(3,4)) == mpq(11,4)
    assert fms(1,2,mpq(3,4)) == mpq(5,4)
    assert fms(1,mpfr(2),3) == mpfr('-1.0')
    assert fms(1,mpc(2),3) == mpc('-1.0+0.0j')

    assert fmma(2,3,4,5) == mpz(26)
    assert fmma(2,3,-4,5) == mpz(-14)
    assert fmma(2.0,3,-4, mpq(5)) == mpfr('-14.0')
    assert fmma(2,3.0,-4,5) == mpfr('-14.0')
    assert fmma(2,3,-4.0,5) == mpfr('-14.0')
    assert fmma(2,mpfr(3),-4.0,5) == mpfr('-14.0')

    pytest.raises(TypeError, lambda: fmma(mpc(2),mpfr(3),-4.0,5))

    assert fmms(2,3,4,5) == mpz(-14)
    assert fmms(2,3,-4,5) == mpz(26)
    assert fmms(2, 3, mpq(1, 2), 5) == mpq(7,2)
    assert fmms(2, 3, mpfr(1.2), 1) == mpfr('4.7999999999999998')

    assert ieee(128).fmma(7,1/7,-1,3/11) == mpfr('0.727272727272727237401994671017746441',113)
    assert ieee(128).fmma(7,mpq(1,7),-1,mpq(3,11)) == mpq(8,11)


def test_trigonometric():
    assert gmpy2.acos(mpc(0.2, 0.2)) == mpc('1.3735541886535356-0.20256635782456389j')
    assert gmpy2.acos(mpc(0.2, 0.2)) == gmpy2.acos(complex(0.2, 0.2))

    assert gmpy2.asin(mpc(0.2,0.2)) == mpc('0.1972421381413611+0.20256635782456389j')
    assert gmpy2.asin(mpc(2.0,0.2)) == mpc('1.4560834209500821+1.3245636864399635j')
    assert gmpy2.asin(mpc(0.2,0.2)) == gmpy2.asin(complex(0.2,0.2))

    assert gmpy2.atan(mpc(2.0, 2.0)) == mpc('1.311223269671635+0.23887786125685909j')
    assert gmpy2.atan(mpc(2.0, 2.0)) == gmpy2.atan(complex(2.0, 2.0))

    c = mpc(2,3)

    assert gmpy2.cos(c) == mpc('-4.189625690968807-9.109227893755337j')

    assert gmpy2.sin(c) == mpc('9.1544991469114301-4.1689069599665647j')

    assert gmpy2.sin_cos(c) == (mpc('9.1544991469114301-4.1689069599665647j'), mpc('-4.189625690968807-9.109227893755337j'))
    assert gmpy2.sin_cos(c) == gmpy2.sin_cos(complex(2,3))
    assert gmpy2.sin_cos(c) == (gmpy2.sin(c), gmpy2.cos(c))

    assert gmpy2.tan(mpc(4,5)) == mpc('8.9834776469715613e-05+1.0000132074347847j')

    assert gmpy2.atanh(mpc(2.0, 3.0)) == mpc('0.14694666622552977+1.3389725222944935j')
    assert gmpy2.atanh(mpc(2.0, 3.0)) == gmpy2.atanh(complex(2, 3))

    assert gmpy2.tanh(mpc(4,5)) == mpc('1.0005630461157933-0.00036520305451130409j')


def test_get_exp():
    ctx = gmpy2.get_context()
    ctx.trap_erange = True

    pytest.raises(gmpy2.RangeError, lambda: get_exp(mpfr('inf')))

    gmpy2.set_context(context())

    assert get_exp(mpfr(5.232)) == 3

    pytest.raises(TypeError, lambda: get_exp(0))

    assert get_exp(mpfr('inf')) == 0
    assert get_exp(mpfr(0)) == 0


def test_set_exp():
    pytest.raises(ValueError, lambda: set_exp(mpfr('1.0'), int(fac(100))))

    gmpy2.set_context(gmpy2.ieee(32))
    ctx = gmpy2.get_context()
    ctx.trap_erange = True

    pytest.raises(gmpy2.RangeError, lambda: set_exp(mpfr('1.0'), 1000))

    ctx.trap_erange = False
    assert set_exp(mpfr('1.0'), 1000) == mpfr('1.0')

    r = mpfr(4.55)

    assert set_exp(r, 4) == mpfr('9.0999999999999996')

    pytest.raises(TypeError, lambda: set_exp(r, mpz(4)))


def test_can_round():
    pytest.raises(TypeError, lambda: can_round(mpfr('1.1'), 10, "spam"))
    pytest.raises(ValueError, lambda: can_round(mpfr('1.1'), 10, 111, 111, 111))
    pytest.raises(ValueError, lambda: can_round(mpfr('1.1'), 10, 1, 111, 111))
    pytest.raises(ValueError, lambda: can_round(mpfr('1.1'), 10, 1, 1, -111))

    x = mpfr('-1.112')

    assert can_round(x, 10, 1, 1, 1)
    assert not can_round(x, 10, 1, 1, 10)


def test_powmod():
    z1, z2 = mpz(5), mpz(2)
    q = mpq(2,3)

    assert powmod(z1, z2, 4) == pow(z1, z2, 4)

    pytest.raises(TypeError, lambda: powmod(z1))
    pytest.raises(TypeError, lambda: powmod(z1, q, 4))


def test_powmod_sec():
    assert powmod_sec(3,3,7) == mpz(6)
    assert powmod_sec(-3,3,7) == mpz(1)
    assert powmod(-3,3,7) == mpz(1)
    assert powmod(3,-3,7) == mpz(6)

    pytest.raises(ValueError, lambda: powmod_sec(3,-3,7))
    pytest.raises(ValueError, lambda: powmod_sec(3,4,8))


def test_is_fermat_prp():
    assert is_fermat_prp(12345,2) is False
    assert is_fermat_prp(113,2)
    assert is_fermat_prp(1234,2) is False

    pytest.raises(TypeError, lambda: is_fermat_prp(1234,'a'))
    pytest.raises(TypeError, lambda: is_fermat_prp(1234, 2, 3))
    pytest.raises(ValueError, lambda: is_fermat_prp(113, 1))
    pytest.raises(ValueError, lambda: is_fermat_prp(-113, 3))
    pytest.raises(ValueError, lambda: is_fermat_prp(339, 3))

    assert is_fermat_prp(mpz(12345),2) is False
    assert is_fermat_prp(113,mpz(2))


def test_is_euler_prp():
    assert is_euler_prp(12345,2) is False
    assert is_euler_prp(113,2)
    assert is_euler_prp(1234,2) is False

    pytest.raises(TypeError, lambda: is_euler_prp(1234,'a'))
    pytest.raises(TypeError, lambda: is_euler_prp(1234, 2, 3))
    pytest.raises(ValueError, lambda: is_euler_prp(113, 1))
    pytest.raises(ValueError, lambda: is_euler_prp(-113, 3))
    pytest.raises(ValueError, lambda: is_euler_prp(339, 3))

    assert is_euler_prp(mpz(12345),2) is False
    assert is_euler_prp(113,mpz(2))


def test_is_strong_prp():
    assert is_strong_prp(12345,2) is False
    assert is_strong_prp(113,2)
    assert is_strong_prp(1234,2) is False

    pytest.raises(TypeError, lambda: is_strong_prp(1234,'a'))
    pytest.raises(TypeError, lambda: is_strong_prp(1234, 2, 3))
    pytest.raises(ValueError, lambda: is_strong_prp(113, 1))
    pytest.raises(ValueError, lambda: is_strong_prp(-113, 3))
    pytest.raises(ValueError, lambda: is_strong_prp(339, 3))

    assert is_strong_prp(mpz(12345),2) is False
    assert is_strong_prp(113,mpz(2))


def test_is_fibonacci_prp():
    assert is_fibonacci_prp(12345, 3, 1) is False
    assert is_fibonacci_prp(113, 3, 1)
    assert is_fibonacci_prp(12345, 3, -1) is False
    assert is_fibonacci_prp(113, 3, -1)

    pytest.raises(ValueError, lambda: is_fibonacci_prp(113, 3, 2))
    pytest.raises(TypeError, lambda: is_fibonacci_prp('a', 3, 2))
    pytest.raises(ValueError, lambda: is_fibonacci_prp(113, 2, 1))

    assert is_fibonacci_prp(113, 2, -1)


def test_is_lucas_prp():
    assert is_lucas_prp(12345, 5, 2) is False
    assert is_lucas_prp(113, 5, 2)

    pytest.raises(ValueError, lambda: is_lucas_prp(12345, 3, 5))


def test_is_is_stronglucas_prp():
    assert is_strong_lucas_prp(12345, 5, 2) is False
    assert is_strong_lucas_prp(113, 5, 2)

    pytest.raises(ValueError, lambda: is_strong_lucas_prp(12345, 3, 5))


def test_is_extra_strong_lucas_prp():
    assert is_extra_strong_lucas_prp(12345, 9) is False
    assert is_extra_strong_lucas_prp(113, 5)

    pytest.raises(ValueError, lambda: is_extra_strong_lucas_prp(12345, 3))


def test_is_selfridge_prp():
    assert is_selfridge_prp(12345) is False
    assert is_selfridge_prp(113)


def test_is_strong_selfridge_prp():
    assert is_strong_selfridge_prp(12345) is False
    assert is_strong_selfridge_prp(113)


def test_is_bpsw_prp():
    assert is_bpsw_prp(12345) is False
    assert is_bpsw_prp(113)


def test_is_strong_bpsw_prp():
    assert is_strong_bpsw_prp(12345) is False
    assert is_strong_bpsw_prp(113)


def test_mpz_from_old_binary():
    assert gmpy2.mpz_from_old_binary(b'\x15\xcd[\x07') == mpz(123456789)
    assert gmpy2.mpz_from_old_binary(b'\x15\xcd[\x07\xff') == mpz(-123456789)

    pytest.raises(TypeError, lambda: mpz_from_old_binary(1))


def test_mpq_from_old_binary():
    assert mpq_from_old_binary(b'\x01\x00\x00\x00)\x98') == mpq(41,152)
    assert mpq_from_old_binary(b'\x01\x00\x00\x80)\x98') == mpq(-41,152)

    pytest.raises(TypeError, lambda: mpq_from_old_binary(1))
    pytest.raises(ValueError, lambda: mpq_from_old_binary(b'aa'))
    pytest.raises(ValueError, lambda: mpq_from_old_binary(b'aaaaaaaaa'))


def test_mpfr_from_old_binary():
    assert mpfr_from_old_binary(b'\x085\x00\x00\x00\x02\x00\x00\x0009\xac\xcc\xcc\xcc\xcc\xcc\xd0') == mpfr('12345.674999999999')
    assert mpfr_from_old_binary(b'\t5\x00\x00\x00\x02\x00\x00\x0009\xac\xcc\xcc\xcc\xcc\xcc\xd0') == mpfr('-12345.674999999999')
    assert mpfr_from_old_binary(b'\n5\x00\x00\x00\x06\x00\x00\x00\x01\x14\xb3\x7fKQ\xf7\x0en') == mpfr('1.5e-17')

    pytest.raises(TypeError, lambda: mpfr_from_old_binary(1))
    pytest.raises(ValueError, lambda: mpfr_from_old_binary(b'aaaaa'))

    assert mpfr_from_old_binary(b'\x04') == mpfr('0.0')


def test_from_binary():
    pytest.raises(TypeError, lambda: from_binary(1))
    pytest.raises(ValueError, lambda: from_binary(b'a'))


def test_phase():
    pytest.raises(TypeError, lambda: phase())
    pytest.raises(TypeError, lambda: phase(3))

    assert phase(mpc(4,5)) == mpfr('0.89605538457134393')
    assert ieee(64).phase(mpc(4,5)) == mpfr('0.89605538457134393')


def test_root_of_unity():
    assert root_of_unity(1,1) == mpc('1.0+0.0j')
    assert root_of_unity(1,2) == mpc('1.0+0.0j')
    assert root_of_unity(2,1) == mpc('-1.0+0.0j')
    assert root_of_unity(3,1) == mpc('-0.5+0.8660254037844386j')
    assert root_of_unity(3,2) == mpc('-0.5-0.8660254037844386j')
    assert root_of_unity(3,3) == mpc('1.0+0.0j')
    assert ieee(128).root_of_unity(3,1) == mpc('-0.5+0.866025403784438646763723170752936161j',(113,113))

    pytest.raises(TypeError, lambda: ieee(128).root_of_unity())
    pytest.raises(TypeError, lambda: ieee(128).root_of_unity('a','b'))


def test_norm():
    pytest.raises(TypeError, lambda: norm())
    pytest.raises(TypeError, lambda: norm(2))

    assert norm(mpc(1,2)) == mpfr('5.0')
    assert ieee(32).norm(mpc(1,2)) == mpfr('5.0',24)


def test_polar():
    pytest.raises(TypeError, lambda: polar())
    pytest.raises(TypeError, lambda: polar(5))
    assert polar(mpc(1,1)) == (mpfr('1.4142135623730951'), mpfr('0.78539816339744828'))


def test_rect():
    pytest.raises(TypeError, lambda: rect())
    pytest.raises(TypeError, lambda: rect(1))

    assert rect(1,1) == mpc('0.54030230586813977+0.8414709848078965j')


def test_proj():
    pytest.raises(TypeError, lambda: proj())
    pytest.raises(TypeError, lambda: proj(1))

    assert proj(mpc(1,1)) == mpc('1.0+1.0j')
    assert proj(mpc(1,2)) == mpc('1.0+2.0j')


def test_is_zero():
    assert is_zero(mpc("0+0j"))
    assert is_zero(mpc("1+0j")) is False
    assert is_zero(mpc("1+1j")) is False
    assert is_zero(mpc("0+1j")) is False

def test_is_nan():
    assert is_nan(mpc("nan+1j"))
    assert is_nan(mpc("1+nanj"))
    assert is_nan(mpc("nan+nanj"))
    assert is_nan(mpc("1+1j")) is False

def test_is_infinite():
    assert is_infinite(mpc("inf+1j"))
    assert is_infinite(mpc("-inf+1j"))
    assert is_infinite(mpc("1+infj"))
    assert is_infinite(mpc("1-infj"))
    assert is_infinite(mpc("inf-infj"))
    assert is_infinite(mpc("1+1j")) is False

def test_is_finite():
    assert is_finite(mpc("0+0j"))
    assert is_finite(mpc("nan+0j")) is False
    assert is_finite(mpc("0+nanj")) is False
    assert is_finite(mpc("0+infj")) is False
    assert is_finite(mpc("inf+3j")) is False


def test_f2q():
    a = mpfr('123.456')

    pytest.raises(TypeError, lambda: f2q('a'))
    pytest.raises(TypeError, lambda: f2q(1,2,3,4))

    assert f2q(a,0.1) == mpz(123)
    assert f2q(a,0.01) == mpz(123)
    assert f2q(a,0.001) == mpq(247,2)
    assert f2q(a,0.0001) == mpq(1358,11)
    assert f2q(a,0.00001) == mpq(7037,57)
    assert f2q(a,0.000001) == mpq(15432,125)
    assert f2q(a,0.0000001) == mpq(15432,125)
    assert f2q(a) == mpq(15432,125)
    assert f2q(2.50000000000008) == mpq(15637498706148,6254999482459)
    assert f2q(2.5000000000000) == mpq(5,2)
    assert f2q(2.50000000000008, 0.001) == mpq(5,2)
    assert f2q(2.50000000000008, -50) == mpq(15637498706148,6254999482459)
    assert f2q(mpfr('0.500000011'), 1e-4) == mpq(1,2)
    assert f2q(mpfr('0.500000011'), 1e-5) == mpq(1,2)
    assert f2q(mpfr('0.500000011'), 1e-6) == mpq(1,2)
    assert f2q(mpfr('0.500000011'), 1e-7) == mpq(1,2)
    assert f2q(mpfr('0.500000011'), 1e-8) == mpq(22727273,45454545)
    assert f2q(mpfr('0.500000011'), 1e-9) == mpq(22727273,45454545)
    assert f2q(mpfr('0.500000011'), 1e-10) == mpq(22727273,45454545)
    assert f2q(mpfr('0.500000011'), 1e-11) == mpq(22727273,45454545)
    assert f2q(mpfr('0.500000011'), 1e-12) == mpq(22727273,45454545)
    assert f2q(mpfr('0.500000011'), 1e-13) == mpq(22727273,45454545)
    assert f2q(mpfr('0.500000011'), 1e-14) == mpq(22727273,45454545)
    assert f2q(mpfr('0.500000011'), 1e-15) == mpq(22727273,45454545)
    assert f2q(mpfr('0.500000011'), 1e-16) == mpq(204545458,409090907)
    assert f2q(mpfr('0.500000011'), 1e-17) == mpq(204545458,409090907)


def test_get_emin_min():
    assert get_emin_min() in (-4611686018427387903, -1073741823)


def test_get_emax_max():
    assert get_emax_max() in (4611686018427387903, 1073741823)


def test_set_sign():
    r = mpfr(4.55)

    assert set_sign(r, False) == mpfr('4.5499999999999998')
    assert set_sign(r, True) == mpfr('-4.5499999999999998')

    pytest.raises(TypeError, lambda: set_sign(mpz(5), True))
    pytest.raises(TypeError, lambda: set_sign(r, 'oiio'))


def test_copy_sign():
    assert copy_sign(mpfr(4), mpfr(-2)) == mpfr('-4.0')

    pytest.raises(TypeError, lambda: copy_sign(mpfr(4), True))


def test_nan():
    x = nan()

    assert is_nan(x)


def test_inf():
    assert inf() == mpfr('inf')
    assert inf(-5) == mpfr('-inf')
    assert inf(mpz(-30)) == mpfr('-inf')

    pytest.raises(TypeError, lambda: inf(mpfr(30)))


def test_check_range():
    r = mpfr(4.55)

    assert check_range(r) == mpfr('4.5499999999999998')

    ctx = gmpy2.get_context()

    assert ctx.check_range(r) == mpfr('4.5499999999999998')

    pytest.raises(TypeError, lambda: ctx.check_range(mpz(5)))


def test_sign():
    a = mpq(3,11)

    assert sign(a) == 1
    assert sign(-a) == -1
    assert sign(mpq(0,5)) == 0

    pytest.raises(TypeError, lambda: sign('str'))

    a = mpfr("12.34")

    assert sign(-1.5) == -1
    assert sign(a) == 1
    assert sign(mpfr(0)) == 0
    assert sign(mpfr('inf')) == 1
    assert sign(mpfr('-inf')) == -1
    assert sign(mpfr('nan')) == 0

    a = mpz(123)
    b = mpz(456)

    assert sign(b-a) == 1
    assert sign(b-b) == 0
    assert sign(a-b) == -1
    assert sign(a) == 1
    assert sign(-a) == -1


def test_acos():
    assert acos(mpfr("0.2")).as_integer_ratio() == (mpz(6167402294989009), mpz(4503599627370496))

    pytest.raises(TypeError, lambda: acos())
    pytest.raises(TypeError, lambda: acos("a"))
    pytest.raises(TypeError, lambda: acos(0,0))

    assert acos(0) == mpfr('1.5707963267948966')
    assert acos(mpz(0)) == mpfr('1.5707963267948966')
    assert acos(mpq(1,2)) == mpfr('1.0471975511965979')
    assert acos(Fraction(1,2)) == mpfr('1.0471975511965979')
    assert is_nan(acos(mpfr("nan")))
    assert is_nan(acos(mpfr("inf")))
    assert is_nan(acos(mpfr("-inf")))

    set_context(context(trap_invalid=True))

    pytest.raises(gmpy2.InvalidOperationError, lambda: acos(mpfr("nan")))
    pytest.raises(gmpy2.InvalidOperationError, lambda: acos(mpfr("inf")))
    pytest.raises(gmpy2.InvalidOperationError, lambda: acos(mpfr("-inf")))

    set_context(context(precision=100))

    assert acos(mpfr("0.2")) == mpfr('1.3694384060045658277761961394221',100)
    assert get_context().precision == 100
    assert get_context().inexact


def test_asin():
    assert gmpy2.asin(mpfr("0.2")).as_integer_ratio() == (mpz(7254683656315453), mpz(36028797018963968))

    pytest.raises(TypeError, lambda: asin())
    pytest.raises(TypeError, lambda: asin("a"))
    pytest.raises(TypeError, lambda: asin(0,0))

    assert asin(0) == mpfr('0.0')
    assert asin(mpz(0)) == mpfr('0.0')
    assert asin(mpq(1,2)) == mpfr('0.52359877559829893')
    assert asin(Fraction(1,2)) == mpfr('0.52359877559829893')
    assert is_nan(asin(mpfr("nan")))
    assert is_nan(asin(mpfr("inf")))
    assert is_nan(asin(mpfr("-inf")))

    set_context(context(trap_invalid=True))

    pytest.raises(gmpy2.InvalidOperationError, lambda: asin(mpfr("nan")))
    pytest.raises(gmpy2.InvalidOperationError, lambda: asin(mpfr("inf")))
    pytest.raises(gmpy2.InvalidOperationError, lambda: asin(mpfr("-inf")))

    set_context(context(precision=100))

    assert asin(mpfr("0.2")) == mpfr('0.20135792079033079145512555221757',100)

    assert get_context().precision == 100
    assert get_context().inexact


def test_atan():
    assert atan(mpfr("0.2")).as_integer_ratio() == (mpz(1777981139569027), mpz(9007199254740992))
    assert atan(mpfr("100")).as_integer_ratio() == (mpz(3514601628432273), mpz(2251799813685248))

    pytest.raises(TypeError, lambda: atan())
    pytest.raises(TypeError, lambda: atan("a"))
    pytest.raises(TypeError, lambda: atan(0,0))

    assert atan(0) == mpfr('0.0')
    assert atan(mpz(0)) == mpfr('0.0')
    assert atan(mpq(1,2)) == mpfr('0.46364760900080609')
    assert atan(Fraction(1,2)) == mpfr('0.46364760900080609')
    assert is_nan(gmpy2.atan(mpfr("nan")))
    assert atan(mpfr("inf")) == mpfr('1.5707963267948966')
    assert atan(mpfr("-inf")) == mpfr('-1.5707963267948966')

    set_context(context(trap_invalid=True))

    pytest.raises(gmpy2.InvalidOperationError, lambda: atan(mpfr("nan")))

    set_context(context(precision=100))

    assert gmpy2.atan(mpfr("0.2")) == mpfr('0.19739555984988075837004976519484',100)
    assert get_context().precision == 100
    assert get_context().inexact


def test_atan2():
    assert atan2(1,2).as_integer_ratio() == (mpz(8352332796509007), mpz(18014398509481984))
    assert atan2(-1,2).as_integer_ratio() == (mpz(-8352332796509007), mpz(18014398509481984))
    assert atan2(1,-2).as_integer_ratio() == (mpz(3015098076232407), mpz(1125899906842624))
    assert atan2(-1,-2).as_integer_ratio() == (mpz(-3015098076232407), mpz(1125899906842624))
    assert atan2(float("0"),float("0")).as_integer_ratio() == (mpz(0), mpz(1))
    assert atan2(float("-0"),float("0")).as_integer_ratio() == (mpz(0), mpz(1))
    assert atan2(float("0"),float("-0")).as_integer_ratio() == (mpz(884279719003555), mpz(281474976710656))
    assert atan2(float("-0"),float("-0")).as_integer_ratio() == (mpz(-884279719003555), mpz(281474976710656))
    assert atan2(float("inf"),float("inf")).as_integer_ratio() == (mpz(884279719003555), mpz(1125899906842624))
    assert atan2(float("-inf"),float("inf")).as_integer_ratio() == (mpz(-884279719003555), mpz(1125899906842624))
    assert atan2(float("inf"),float("-inf")).as_integer_ratio() == (mpz(2652839157010665), mpz(1125899906842624))
    assert atan2(float("-inf"),float("-inf")).as_integer_ratio() == (mpz(-2652839157010665), mpz(1125899906842624))


def test_cos():
    assert cos(mpfr("0.2")).as_integer_ratio() == (mpz(4413827474764093), mpz(4503599627370496))
    assert cos(mpfr("20")).as_integer_ratio() == (mpz(7351352886077503), mpz(18014398509481984)) or (sys.platform == 'win32')
    assert cos(mpfr("2000")).as_integer_ratio() == (mpz(-3309781376808469), mpz(9007199254740992))

    pytest.raises(TypeError, lambda: cos())
    pytest.raises(TypeError, lambda: cos("a"))
    pytest.raises(TypeError, lambda: cos(0,0))

    assert cos(0) == mpfr('1.0')
    assert cos(mpz(0)) == mpfr('1.0')
    assert cos(mpq(1,2)) == mpfr('0.87758256189037276')
    assert cos(Fraction(1,2)) == mpfr('0.87758256189037276')
    assert is_nan(cos(mpfr("nan")))
    assert is_nan(cos(mpfr("inf")))
    assert is_nan(cos(mpfr("-inf")))

    set_context(context(trap_invalid=True))

    pytest.raises(gmpy2.InvalidOperationError, lambda: cos(mpfr("nan")))
    pytest.raises(gmpy2.InvalidOperationError, lambda: cos(mpfr("inf")))
    pytest.raises(gmpy2.InvalidOperationError, lambda: cos(mpfr("-inf")))

    set_context(context(precision=100))

    assert cos(mpfr("0.2")) == mpfr('0.98006657784124163112419651674809',100)
    assert get_context().precision == 100
    assert get_context().inexact


def test_cot():
    assert cot(mpfr("0.2")).as_integer_ratio() == (mpz(173569956714485), mpz(35184372088832))
    assert cot(gmpy2.const_pi()).as_integer_ratio() == (mpz(-8165619676597685), mpz(1))
    assert cot(1) == mpfr('0.64209261593433076')
    assert cot(float('0')) == mpfr('inf')
    assert cot(float('-0')) == mpfr('-inf')
    assert cot(mpfr('0')) == mpfr('inf')
    assert cot(mpfr('-0')) == mpfr('-inf')


def test_csc():
    r2 = mpfr('5.6')

    assert csc(r2) == mpfr('-1.5841166632383596')


def test_sec():
    r2 = mpfr('5.6')

    assert sec(r2) == mpfr('1.2893811186238056')


def test_sin():
    r = mpfr(5.6)

    assert sin(r) == mpfr('-0.63126663787232162')
    assert sin(r) == sin(5.6)


def test_sin_cos():
    r = mpfr(5.6)

    assert sin_cos(r) == (mpfr('-0.63126663787232162'), mpfr('0.77556587851024961'))
    assert sin_cos(r) == sin_cos(5.6)
    assert sin_cos(r) == (sin(r), cos(r))


def test_tan():
    r = mpfr(5.6)

    assert tan(r) == mpfr('-0.8139432836897027')


def test_acosh():
    r = mpfr(5.6)

    assert acosh(r) == mpfr('2.4078447868719399')

def test_asinh():
    r = mpfr(5.6)

    assert asinh(r) == mpfr('2.4237920435875173')


def test_atanh():
    assert atanh(mpfr(0.365)) == mpfr('0.38264235436318422')
    assert atanh(mpfr(0.365)) == atanh(0.365)


def test_cosh():
    r = mpfr(5.6)

    assert cosh(r) == mpfr('135.2150526449345')
    assert cosh(r) == cosh(5.6)


def test_coth():
    r = mpfr(5.6)

    assert coth(r) == mpfr('1.0000273487661038')


def test_csch():
    r = mpfr(5.6)

    assert csch(r) == mpfr('0.0073958285649757295')


def test_degrees():
    rad = mpfr(1.57)
    ctx = get_context()

    assert ctx.degrees(rad) == mpfr('89.954373835539243')
    assert degrees(rad) == mpfr('89.954373835539243')
    assert degrees(1) == mpfr('57.295779513082323')


def test_radians():
    deg = mpfr(90)
    ctx = get_context()

    assert ctx.radians(deg) == mpfr('1.5707963267948966')
    assert radians(deg) == mpfr('1.5707963267948966')
    assert radians(45) == mpfr('0.78539816339744828')
    assert radians(mpz(20)) == mpfr('0.3490658503988659')
    assert radians(mpfr('inf')) == mpfr('inf')
    assert is_nan(radians(mpfr('nan')))


def test_sech():
    r = mpfr(5.6)

    assert sech(r) == mpfr('0.0073956263037217584')


def test_sinh():
    r = mpfr(5.6)

    assert sinh(r) == mpfr('135.21135478121803')
    assert sinh(r) == gmpy2.sinh(5.6)


def test_sinh_cosh():
    r = mpfr(5.6)

    assert sinh_cosh(r) == (mpfr('135.21135478121803'), mpfr('135.2150526449345'))
    assert sinh_cosh(r) == sinh_cosh(5.6)
    assert sinh_cosh(r) == (sinh(r), cosh(r))


def test_tanh():
    r = mpfr(5.6)

    assert tanh(r) == mpfr('0.99997265198183083')


def test_c_divmod():
    a = mpz(123)
    b = mpz(456)

    pytest.raises(TypeError, lambda: c_divmod(1))
    pytest.raises(TypeError, lambda: c_divmod(1, 'a'))
    pytest.raises(ZeroDivisionError, lambda: c_divmod(a,0))

    assert c_divmod(b,a) == (mpz(4), mpz(-36))
    assert c_divmod(b,-a) == (mpz(-3), mpz(87))
    assert c_divmod(-b,a) == (mpz(-3), mpz(-87))
    assert c_divmod(-b,-a) == (mpz(4), mpz(36))


def test_c_div():
    a = mpz(123)
    b = mpz(456)

    pytest.raises(TypeError, lambda: c_div(1))
    pytest.raises(TypeError, lambda: c_div(1, 'a'))
    pytest.raises(ZeroDivisionError, lambda: c_div(a,0))

    assert c_div(b,a) == mpz(4)
    assert c_div(b,-a) == mpz(-3)
    assert c_div(-b,a) == mpz(-3)
    assert c_div(-b,-a) == mpz(4)


def test_c_mod():
    a = mpz(123)
    b = mpz(456)

    pytest.raises(TypeError, lambda: c_mod(1))
    pytest.raises(TypeError, lambda: c_mod(1, 'a'))
    pytest.raises(ZeroDivisionError, lambda: c_mod(a,0))

    assert c_mod(b,a) == mpz(-36)
    assert c_mod(b,-a) == mpz(87)
    assert c_mod(-b,a) == mpz(-87)
    assert c_mod(-b,-a) == mpz(36)


def test_f_divmod():
    a = mpz(123)
    b = mpz(456)

    pytest.raises(TypeError, lambda: f_divmod(1))
    pytest.raises(TypeError, lambda: f_divmod(1, 'a'))
    pytest.raises(ZeroDivisionError, lambda: f_divmod(a,0))

    assert f_divmod(b,a) == (mpz(3), mpz(87))
    assert f_divmod(b,-a) == (mpz(-4), mpz(-36))
    assert f_divmod(-b,a) == (mpz(-4), mpz(36))
    assert f_divmod(-b,-a) == (mpz(3), mpz(-87))


def test_f_div():
    a = mpz(123)
    b = mpz(456)

    pytest.raises(TypeError, lambda: f_div(1))
    pytest.raises(TypeError, lambda: f_div(1, 'a'))
    pytest.raises(ZeroDivisionError, lambda: f_div(a,0))

    assert f_div(b,a) == mpz(3)
    assert f_div(b,-a) == mpz(-4)
    assert f_div(-b,a) == mpz(-4)
    assert f_div(-b,-a) == mpz(3)


def test_f_mod():
    a = mpz(123)
    b = mpz(456)

    pytest.raises(TypeError, lambda: f_mod(1))
    pytest.raises(TypeError, lambda: f_mod(1, 'a'))
    pytest.raises(ZeroDivisionError, lambda: f_mod(a,0))

    assert f_mod(b,a) == mpz(87)
    assert f_mod(b,-a) == mpz(-36)
    assert f_mod(-b,a) == mpz(36)
    assert f_mod(-b,-a) == mpz(-87)


def test_t_divmod():
    a = mpz(123)
    b = mpz(456)

    pytest.raises(TypeError, lambda: t_divmod(1))
    pytest.raises(TypeError, lambda: t_divmod(1, 'a'))
    pytest.raises(ZeroDivisionError, lambda: t_divmod(a,0))

    assert t_divmod(b,a) == (mpz(3), mpz(87))
    assert t_divmod(b,-a) == (mpz(-3), mpz(87))
    assert t_divmod(-b,a) == (mpz(-3), mpz(-87))
    assert t_divmod(-b,-a) == (mpz(3), mpz(-87))


def test_t_div():
    a = mpz(123)
    b = mpz(456)

    pytest.raises(TypeError, lambda: t_div(1))
    pytest.raises(TypeError, lambda: t_div(1, 'a'))
    pytest.raises(ZeroDivisionError, lambda: t_div(a,0))

    assert t_div(b,a) == mpz(3)
    assert t_div(b,-a) == mpz(-3)
    assert t_div(-b,a) == mpz(-3)
    assert t_div(-b,-a) == mpz(3)


def test_t_mod():
    a = mpz(123)
    b = mpz(456)

    pytest.raises(TypeError, lambda: t_mod(1))
    pytest.raises(TypeError, lambda: t_mod(1, 'a'))
    pytest.raises(ZeroDivisionError, lambda: t_mod(a,0))

    assert t_mod(b,a) == mpz(87)
    assert t_mod(b,-a) == mpz(87)
    assert t_mod(-b,a) == mpz(-87)
    assert t_mod(-b,-a) == mpz(-87)


def test_get_max_precision():
    assert gmpy2.get_max_precision() > 53


def test_free_cache():
    assert free_cache() is None


def test_gcd():
    a = mpz(123)
    b = mpz(456)

    assert gcd(1,2,3) == mpz(1)
    assert gcd(2, 4, 6) == mpz(2)

    pytest.raises(TypeError, lambda: gcd(1,'a'))

    assert gcd(123,456) == mpz(3)
    assert gcd(a,b) == mpz(3)


def test_lcm():
    a = mpz(123)
    b = mpz(456)

    assert lcm(1,2,3) == mpz(6)
    assert lcm(2, 3, 4) == mpz(12)

    pytest.raises(TypeError, lambda: lcm(1,'a'))

    assert lcm(a,b) == mpz(18696)
    assert lcm(123,456) == mpz(18696)


def test_gcdext():
    a = mpz(123)
    b = mpz(456)

    pytest.raises(TypeError, lambda: gcdext(1,2,3))
    pytest.raises(TypeError, lambda: gcdext(1,'a'))

    temp = gcdext(a,b)

    assert temp[0] == a*temp[1] + b*temp[2]

    temp = gcdext(123,456)

    assert temp[0] == a*temp[1] + b*temp[2]


def test_divm():
    a = mpz(123)
    b = mpz(456)

    assert divm(b,a,20) == mpz(12)

    pytest.raises(TypeError, lambda: divm(a,b,100,5))
    pytest.raises(TypeError, lambda: divm(a,b,'a'))
    pytest.raises(ZeroDivisionError, lambda: divm(a,b,100))

    assert divm(6,12,14) == mpz(4)
    assert divm(0,1,2) == mpz(0)
    assert divm(4,8,20) == mpz(3)


def test_fac():
    pytest.raises(OverflowError, lambda: fac(-7))
    pytest.raises(TypeError, lambda: fac('a'))

    assert fac(7) == mpz(5040)


def test_double_fac():
    pytest.raises(OverflowError, lambda: double_fac(-7))
    pytest.raises(TypeError, lambda: double_fac('a'))

    assert double_fac(7) == mpz(105)
    assert double_fac(7) * gmpy2.double_fac(8) == mpz(40320)
    assert fac(8) == mpz(40320)


def test_primorial():
    pytest.raises(OverflowError, lambda: primorial(-7))
    pytest.raises(TypeError, lambda: primorial('a'))

    assert primorial(7) == mpz(210)


def test_multi_fac():
    pytest.raises(TypeError, lambda: multi_fac(-7))
    pytest.raises(TypeError, lambda: multi_fac(7,'a'))
    pytest.raises(OverflowError, lambda: multi_fac(7,-1))
    pytest.raises(OverflowError, lambda: multi_fac(-7,1))
    pytest.raises(TypeError, lambda: multi_fac('a'))
    pytest.raises(TypeError, lambda: multi_fac(10))
    pytest.raises(TypeError, lambda: multi_fac(10,11,12))

    assert multi_fac(17,4) == mpz(9945)


def test_fib():
    pytest.raises(OverflowError, lambda: fib(-2))

    assert fib(17) == mpz(1597)


def test_fib2():
    pytest.raises(OverflowError, lambda: fib2(-2))

    assert fib2(17) == (mpz(1597), mpz(987))


def test_lucas():
    pytest.raises(OverflowError, lambda: lucas(-2))

    assert lucas(17) == mpz(3571)


def test_lucas2():
    pytest.raises(OverflowError, lambda: lucas2(-2))

    assert lucas2(17) == (mpz(3571), mpz(2207))


def test_bincoef():
    pytest.raises(TypeError, lambda: bincoef(1))
    pytest.raises(TypeError, lambda: bincoef(1,2,3))

    assert [bincoef(10,i) for i in range(10)] == [1, 10, 45, 120, 210,
                                                  252, 210, 120, 45, 10]
    assert bincoef(1111111111111111111111,
                   2) == mpz(617283950617283950616604938271604938271605)


def test_comb():
    pytest.raises(OverflowError, lambda: comb(3,-1))
    pytest.raises(TypeError, lambda: comb('a',4))

    assert comb(8,4) == mpz(70)


def test_isqrt():
    a = mpz(123)

    assert isqrt(a) == 11
    assert isqrt(123) == 11

    pytest.raises(ValueError, lambda: isqrt(-1))
    pytest.raises(ValueError, lambda: isqrt(mpz(-1)))
    pytest.raises(TypeError, lambda: isqrt('a'))


def test_isqrt_rem():
    a = mpz(123)
    b = mpz(456)

    assert isqrt_rem(a) == (mpz(11), mpz(2))
    assert isqrt_rem(b) == (mpz(21), mpz(15))

    pytest.raises(ValueError, lambda: isqrt_rem(-1))
    pytest.raises(ValueError, lambda: isqrt_rem(mpz(-1)))
    pytest.raises(TypeError, lambda: isqrt_rem('a'))
    pytest.raises(ValueError, lambda: isqrt_rem(mpz(-1)))


def test_remove():
    a = mpz(123)
    b = mpz(456)

    assert remove(a,2) == (mpz(123), 0)
    assert remove(a,mpz(2)) == (mpz(123), 0)
    assert remove(a,3) == (mpz(41), 1)
    assert remove(b,2) == (mpz(57), 3)
    assert remove(b,3) == (mpz(152), 1)

    pytest.raises(ValueError, lambda: remove(b,1))
    pytest.raises(ValueError, lambda: remove(b,mpz(1)))
    pytest.raises(ValueError, lambda: remove(b,0))

    assert remove(b,789) == (mpz(456), 0)

    pytest.raises(ValueError, lambda: remove(b,-3))
    pytest.raises(TypeError, lambda: remove(b,float('NaN')))
    pytest.raises(ValueError, lambda: remove(3,-1))
    pytest.raises(TypeError, lambda: remove(3))
    pytest.raises(TypeError, lambda: remove())


def test_invert():
    a = mpz(123)
    b = mpz(456)

    assert invert(a,100) == mpz(87)
    assert invert(a,mpz(100)) == mpz(87)

    pytest.raises(ZeroDivisionError, lambda: invert(b,mpz(100)))
    pytest.raises(ZeroDivisionError, lambda: invert(b,mpz(0)))
    pytest.raises(TypeError, lambda: invert(3))
    pytest.raises(TypeError, lambda: invert())
    pytest.raises(ZeroDivisionError, lambda: invert(456,0))
    pytest.raises(TypeError, lambda: invert(456,'a'))
    pytest.raises(ZeroDivisionError, lambda: invert(456,100))

    assert invert(123,100) == mpz(87)


def test_divexact():
    a = mpz(123)

    pytest.raises(TypeError, lambda: divexact(2))
    pytest.raises(TypeError, lambda: divexact(2, 'a'))
    pytest.raises(ZeroDivisionError, lambda: divexact(a,0))
    pytest.raises(ZeroDivisionError, lambda: divexact(a,mpz(0)))
    pytest.raises(ZeroDivisionError, lambda: divexact(123,0))

    aa = mpz('1234567912345678912345679')
    bb = mpz('789789789789789789789789')
    cc = aa*bb

    assert divexact(cc,aa) == 789789789789789789789789

    aa = 1234567912345678912345679
    bb = 789789789789789789789789
    cc = aa*bb

    assert divexact(cc,aa) == 789789789789789789789789


def test_next_prime():
    pytest.raises(TypeError, lambda: next_prime('a'))

    assert next_prime(mpz(2)) == mpz(3)
    assert next_prime(2) == mpz(3)
    assert next_prime(1000000) == mpz(1000003)
    assert next_prime(2357*7069-1) != 2357*7069


def test_iroot():
    a = mpz(123)
    b = mpz(456)

    pytest.raises(TypeError, lambda: iroot(1,2,3))
    pytest.raises(ValueError, lambda: iroot(-9,2))
    pytest.raises(ValueError, lambda: iroot(9,0))

    assert [(iroot(a,i+1),gmpy2.iroot(b,i+1))
            for i in range(5)] == [((mpz(123), True), (mpz(456), True)),
                                   ((mpz(11), False), (mpz(21), False)),
                                   ((mpz(4), False), (mpz(7), False)),
                                   ((mpz(3), False), (mpz(4), False)),
                                   ((mpz(2), False), (mpz(3), False))]
    assert iroot(9,2) == (mpz(3), True)


def test_iroot_rem():
    a = mpz(123)

    pytest.raises(TypeError, lambda: iroot_rem(1,2,3))
    pytest.raises(ValueError, lambda: iroot_rem(-9,2))
    pytest.raises(ValueError, lambda: iroot_rem(9,0))

    assert iroot_rem(a,2) == (mpz(11), mpz(2))
    assert iroot_rem(a,3) == (mpz(4), mpz(59))
    assert iroot_rem(a*a,2) == (mpz(123), mpz(0))


def test_jacobi():
    pytest.raises(TypeError, lambda: jacobi('a', 10))
    pytest.raises(ValueError, lambda: jacobi(10,-3))
    pytest.raises(TypeError, lambda: jacobi(3))
    pytest.raises(TypeError, lambda: jacobi())

    assert jacobi(10,3) == 1


def test_kronecker():
    pytest.raises(TypeError, lambda: gmpy2.kronecker('a', 10))

    assert kronecker(10,3) == 1
    assert kronecker(10,-3) == 1

    pytest.raises(TypeError, lambda: kronecker(3))
    pytest.raises(TypeError, lambda: kronecker())

    aaa = 10**20
    bbb = aaa + 39

    assert jacobi(aaa,bbb) == 1
    assert legendre(aaa,bbb) == 1
    assert kronecker(aaa,bbb) == 1


def test_legendre():
    pytest.raises(TypeError, lambda: legendre('a', 10))

    assert legendre(10,3) == 1

    pytest.raises(ValueError, lambda: legendre(10,-3))
    pytest.raises(TypeError, lambda: legendre(3))
    pytest.raises(TypeError, lambda: legendre())
