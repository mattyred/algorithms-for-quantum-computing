from math import gcd, log2, ceil
import numpy as np
import random
import cudaq
from cudaq import *
import fractions
import matplotlib.pyplot as plt
import contfrac

def shors_algorithm(N, initial, quantum):
    """ Factor N using Shor's algorithm with initial starting value and choice of
    using either classical or quantum approach for the period finding step
    Parameters
    ----------
    N: int
        Integer to be factored (assumed to be non-prime and >1)
    initial: int
        Initial choice of the random integer between 2 and N-1
    quantum: boolean
        True if we will call the quantum order-finding algorithm, and false if we call the classical one for step 3.

    Returns
    -------
    a1, a2: int
        Non-trivial factors of N
    """

    # 0. Check to see if N is even.
    if N % 2 == 0:
        divisor1 = 2
        divisor2 = N // 2
        print("Found factors:", divisor1, divisor2)
        return (divisor1, divisor2)

    attempts = [initial]
    while (True):
        # 1. Select a random integer between 2 and N-1
        if len(attempts) == 1:
            a = initial
        else:
            a = random.choice(
                [n for n in range(N - 1) if n not in attempts and n != 1])

        # 2. See if the integer selected in step 1 happens to factor N
        print("Trying a =", a)
        divisor1 = gcd(a, N)
        if divisor1 != 1:
            divisor2 = N // divisor1
            print("Found factors of N={} by chance: {} and {}".format(
                N, divisor1, divisor2))
            return (divisor1, divisor2)

        # 3. Find the order of a mod N (i.e., r, where a^r = 1 (mod N))
        if quantum == True:
            r = find_order_quantum(a, N)
        else:
            r = find_order_classical(a, N)
        print("The order of a = {} is {}".format(a, r))

        # 4. If the order of a is found and it is
        # * even and
        # * not a^(r/2) = -1 (mod N),
        # then test a^(r/2)-1 and a^(r/2)+1 to see if they share factors with N.
        # We also want to rule out the case of finding the trivial factors: 1 and N.
        divisor1, divisor2 = test_order(a, r, N)
        if (divisor1 != 0):  # test_order will return a 0 if no factor is found
            print("Found factors of N = {}: {} and {}".format(
                N, divisor1, divisor2))
            return divisor1, divisor2

        # 5. Repeat
        print("retrying...")
        attempts.append(a)

def test_order(a, r, N):
    """Checks whether or not a^(r/2)+1 or a^(r/2)-1 share a non-trivial common factor with N
    Parameters
    ----------
    a: int
    r: int
    N: int

    Returns
    -------
    int, int factors of N, if found; 0,0 otherwise
    """

    if r != None and (r % 2 == 0) and a**r % N == 1:
        if (a**(int(r / 2))) % N != -1:
            possible_factors = [gcd(r - 1, N), gcd(r + 1, N)]
            for test_factor in possible_factors:
                if test_factor != 1 and test_factor != N:
                    return test_factor, N // test_factor
    # period did not produce a factor
    else:
        print('No non-trivial factor found')
        return 0, 0

def find_order_classical(a, N):
    """A naive classical method to find the order r of a (mod N).
    Parameters
    ----------
    a: int
        an integer in the interval [2,N-1]
    N: int

    Returns
    -------
    r: int
        Period of a^x (mod N)
    """
    assert 1 < a and a < N
    r = 1
    y = a
    while y != 1:
        y = y * a % N
        r += 1
    return r

my_integer = 123  #edit this value to try out a few examples
# Edit the value in the line below to try out different initial guesses for a.
# What happens when you choose a = 42 for the integer 123?
# What happens when you choose a = 100 for the integer 123?
initial_value_to_start = 42  # edit this value; it should be less than my_integer

shors_algorithm(my_integer, initial_value_to_start, False)