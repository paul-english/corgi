from decimal import Decimal

import numpy as np

# Implementation reference:
# http://stackoverflow.com/a/29955556/1072288

LOG10_OF_2 = Decimal(
    3.010299956639811952137388947244930267681898814621085413104274611e-1)


def sigfig_round(x, n, ignore_left_of_decimal=False, eps=1e-7):

    if not (type(n) is int or np.issubdtype(n, np.integer)):
        raise TypeError("sigfig_round: n must be an integer.")

    if not np.all(np.isreal(x)):
        raise TypeError("sigfig_round: all x must be real.")

    if n <= 0:
        raise ValueError("sigfig_round: n must be positive.")

    if ignore_left_of_decimal:
        # Note: doesn't return true significant figure representation, as it's not
        # counting left of decimal sigfigs.
        left_of_decimal = np.trunc(x)
        right_of_decimal = x - left_of_decimal
        return left_of_decimal + sigfig_round(right_of_decimal, n)
    else:
        mantissas, binary_exponents = np.frexp(x)
        decimal_exponents = (LOG10_OF_2 * binary_exponents).astype(np.float64)
        int_parts = np.floor(decimal_exponents)
        mantissas *= 10.0**(decimal_exponents - int_parts)
        return np.around(mantissas.values, decimals=n - 1) * 10.0**int_parts
