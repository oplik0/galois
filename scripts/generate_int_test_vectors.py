"""
Script to generate unit test vectors for number theoretic functions.

* `sudo apt install sagemath`
"""
import json
import os
import pickle
import random
import shutil

import sage
import numpy as np
from sage.all import Integer, Integers, xgcd, lcm, prod, isqrt, log, crt, euler_phi, prime_range, nth_prime, previous_prime, is_prime
from sage.crypto.util import carmichael_lambda

PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "tests")
FOLDER = os.path.join(PATH, "data")
if os.path.exists(FOLDER):
    shutil.rmtree(FOLDER)
os.mkdir(FOLDER)

SEED = 123456789


def set_seed(seed):
    """Update the RNG seeds so the LUT is reproducible"""
    np.random.seed(seed)
    random.seed(seed)


def save_pickle(d, folder, name):
    with open(os.path.join(folder, name), "wb") as f:
        pickle.dump(d, f)


###############################################################################
# Math functions
###############################################################################

set_seed(SEED + 101)
X = [random.randint(-1000, 1000) for _ in range(20)] + [random.randint(-1000, 1_000_000_000) for _ in range(20)]
Y = [random.randint(-1000, 1000) for _ in range(20)] + [random.randint(-1000, 1_000_000_000) for _ in range(20)]
D = [0,]*len(X)
S = [0,]*len(X)
T = [0,]*len(X)
for i in range(len(X)):
    x = X[i]
    y = Y[i]
    d, s, t = xgcd(x, y)
    D[i] = int(d)
    S[i] = int(s)
    T[i] = int(t)
d = {"X": X, "Y": Y, "D": D, "S": S, "T": T}
save_pickle(d, FOLDER, "egcd.pkl")

set_seed(SEED + 102)
X = [[random.randint(-1000, 1000) for _ in range(random.randint(2, 6))] for _ in range(20)] + [[random.randint(-1000, 1_000_000) for _ in range(random.randint(2, 6))] for _ in range(20)]
Z = [0,]*len(X)
for i in range(len(X)):
    x = X[i]
    z = lcm(x)
    Z[i] = int(z)
d = {"X": X, "Z": Z}
save_pickle(d, FOLDER, "lcm.pkl")

set_seed(SEED + 103)
X = [[random.randint(-1000, 1000) for _ in range(random.randint(2, 6))] for _ in range(20)] + [[random.randint(-1000, 1_000_000) for _ in range(random.randint(2, 6))] for _ in range(20)]
Z = [0,]*len(X)
for i in range(len(X)):
    x = X[i]
    z = prod(x)
    Z[i] = int(z)
d = {"X": X, "Z": Z}
save_pickle(d, FOLDER, "prod.pkl")

set_seed(SEED + 104)
X = [random.randint(-1000, 1000) for _ in range(20)] + [random.randint(-1000, 1_000_000) for _ in range(20)]
E = [random.randint(0, 1_000) for _ in range(40)]
M = [random.randint(-1000, 1000) for _ in range(20)] + [random.randint(-1000, 1_000_000) for _ in range(20)]
Z = [0,]*len(X)
for i in range(len(X)):
    x = X[i]
    e = E[i]
    m = M[i]
    z = pow(x, e, m)
    Z[i] = int(z)
d = {"X": X, "E": E, "M": M, "Z": Z}
save_pickle(d, FOLDER, "power.pkl")

set_seed(SEED + 105)
X = [random.randint(0, 1000) for _ in range(20)] + [random.randint(1000, 1_000_000_000) for _ in range(20)]
Z = [0,]*len(X)
for i in range(len(X)):
    x = X[i]
    z = isqrt(x)
    Z[i] = int(z)
d = {"X": X, "Z": Z}
save_pickle(d, FOLDER, "isqrt.pkl")

set_seed(SEED + 106)
X = [random.randint(0, 1000) for _ in range(20)] + [random.randint(1000, 1_000_000_000) for _ in range(20)]
R = [random.randint(1, 6) for _ in range(40)]
Z = [0,]*len(X)
for i in range(len(X)):
    x = X[i]
    r = R[i]
    z = Integer(x).nth_root(r, truncate_mode=True)[0]
    Z[i] = int(z)
d = {"X": X, "R": R, "Z": Z}
save_pickle(d, FOLDER, "iroot.pkl")

set_seed(SEED + 107)
X = [random.randint(1, 1000) for _ in range(20)] + [random.randint(1000, 1_000_000_000) for _ in range(20)]
B = [random.randint(2, 6) for _ in range(40)]
Z = [0,]*len(X)
for i in range(len(X)):
    x = X[i]
    b = B[i]
    z = log(Integer(x), b)
    Z[i] = int(z)
d = {"X": X, "B": B, "Z": Z}
save_pickle(d, FOLDER, "ilog.pkl")

set_seed(SEED + 108)
N = [random.randint(2, 6) for _ in range(40)]
X = [[random.randint(0, 1000) for _ in range(N[i])] for i in range(20)] + [[random.randint(0, 1_000_000) for _ in range(N[20 + i])] for i in range(20)]  # Remainder
Y = [[random.randint(10, 1000) for _ in range(N[i])] for i in range(20)] + [[random.randint(1000, 1_000_000) for _ in range(N[20 + i])] for i in range(20)]  # Modulus
Z = [0,]*len(X)  # The solution
for i in range(len(X)):
    X[i] = [X[i][j] % Y[i][j] for j in range(len(X[i]))]  # Ensure a is within [0, m)
    try:
        z = crt(X[i], Y[i])
        Z[i] = int(z)
    except:
        Z[i] = None
d = {"X": X, "Y": Y, "Z": Z}
save_pickle(d, FOLDER, "crt.pkl")


###############################################################################
# Number theory functions
###############################################################################

set_seed(SEED + 201)
X = [random.randint(1, 1_000_000_000) for _ in range(20)]
Z = [0,]*len(X)
for i in range(len(X)):
    x = X[i]
    z = euler_phi(x)
    Z[i] = int(z)
d = {"X": X, "Z": Z}
save_pickle(d, FOLDER, "euler_phi.pkl")

set_seed(SEED + 202)
X = [random.randint(1, 1_000_000_000) for _ in range(20)]
Z = [0,]*len(X)
for i in range(len(X)):
    x = X[i]
    z = carmichael_lambda(x)
    Z[i] = int(z)
d = {"X": X, "Z": Z}
save_pickle(d, FOLDER, "carmichael_lambda.pkl")

set_seed(SEED + 203)
X = list(range(1, 257)) + [random.randint(1, 1_000_000_000) for _ in range(20)]
Z = [False,]*len(X)
for i in range(len(X)):
    x = X[i]
    z = Integers(X[i]).multiplicative_group_is_cyclic()
    Z[i] = bool(z)
d = {"X": X, "Z": Z}
save_pickle(d, FOLDER, "is_cyclic.pkl")


###############################################################################
# Prime number functions
###############################################################################

set_seed(SEED + 301)
X = [random.randint(1, 1000) for _ in range(10)]
Z = [0,]*len(X)
for i in range(len(X)):
    x = X[i]
    z = prime_range(x)  # Returns primes 0 <= p < x
    if is_prime(x):  # galois.primes() returns 0 <= p <= x
        z.append(x)
    Z[i] = [int(zz) for zz in z]
d = {"X": X, "Z": Z}
save_pickle(d, FOLDER, "primes.pkl")

set_seed(SEED + 302)
X = [random.randint(1, 1000) for _ in range(20)]
Z = [0,]*len(X)
for i in range(len(X)):
    x = X[i]
    z = nth_prime(x)
    Z[i] = int(z)
d = {"X": X, "Z": Z}
save_pickle(d, FOLDER, "kth_prime.pkl")

set_seed(SEED + 303)
X = [random.randint(1, 100) for _ in range(20)] + [random.randint(100, 1_000_000) for _ in range(20)]
Z = [0,]*len(X)
for i in range(len(X)):
    x = X[i]
    z = previous_prime(x)  # Returns z < x
    if is_prime(x):  # galois.prev_prime() returns z <= x
        z = x
    Z[i] = int(z)
d = {"X": X, "Z": Z}
save_pickle(d, FOLDER, "prev_prime.pkl")
