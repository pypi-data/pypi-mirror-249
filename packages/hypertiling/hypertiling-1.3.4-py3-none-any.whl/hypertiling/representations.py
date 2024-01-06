import numpy as np
from hypertiling.check_numba import NumbaChecker
from numpy import array as nparray


def valid_weierstrass_point(point):
    '''Check that a point is a valid Weierstrass point'''
    [t, x, y] = point
    return t > 0 and (1 + x * x + y * y) * t * t > 1


@NumbaChecker("float64[::1](complex128)")
def p2w(z: np.complex128) -> np.array:
    '''Convert Poincare to Weierstraß representation '''
    x, y = z.real, z.imag
    xx = x * x
    yy = y * y
    factor = 1 / (1 - xx - yy)
    return factor * nparray([(1 + xx + yy), 2 * x, 2 * y])


@NumbaChecker("complex128(float64[:])")
def w2p(point: np.array) -> np.complex128:
    '''Convert Weierstraß to Poincare representation '''
    [t, x, y] = point
    factor = 1 / (1 + t)
    return np.complex128(complex(x * factor, y * factor))


@NumbaChecker("float64[::1](complex128)")
def p2w_xyt(z: np.complex128) -> np.array:
    '''Convert Poincare to Weierstraß representation '''
    x, y = z.real, z.imag
    xx = x * x
    yy = y * y
    factor = 1 / (1 - xx - yy)
    return factor * nparray([2 * x, 2 * y, (1 + xx + yy)])


@NumbaChecker("complex128(float64[:])")
def w2p_xyt(point: np.array) -> np.complex128:
    '''Convert Weierstraß to Poincare representation '''
    [x, y, t] = point
    factor = 1 / (1 + t)
    return np.complex128(complex(x * factor, y * factor))



def p2w_xyt_vector(z_list):
    # Poincare to Weierstrass
    return np.array([p2w_xyt(x) for x in z_list])


def w2p_xyt_vector(xyt_list):
    # Weierstrass to Poincare
    return np.array([w2p_xyt(z) for z in xyt_list])