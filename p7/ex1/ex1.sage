# Q1 - How hard is factoring?
#
# For each k, generate two random primes of k/2 bits, multiply them into a
# k-bit modulus N and time factor(N). Run with:  sage ex1.sage
#
# Sage's factor() on an Integer calls PARI's factorint (ECM + MPQS).

import time

KS = [128, 160, 192, 224, 256]
TRIALS = 3


def rsa_modulus(k):
    """Two distinct random k/2-bit primes whose product has exactly k bits."""
    lo, hi = 2^(k // 2 - 1), 2^(k // 2) - 1
    while True:
        p = random_prime(hi, lbound=lo)
        q = random_prime(hi, lbound=lo)
        N = p * q
        if p != q and N.nbits() == k:
            return p, q, N


print("%5s | %s" % ("k", "time per trial (s)"))
results = {}
for k in KS:
    times = []
    for _ in range(TRIALS):
        p, q, N = rsa_modulus(k)
        start = time.perf_counter()
        F = factor(N)
        times.append(time.perf_counter() - start)
        assert sorted(f for f, _ in F) == sorted([p, q])
    results[k] = sum(times) / len(times)
    print("%5d | %s | mean %.3f" % (k, ", ".join("%.3f" % t for t in times),
                                   results[k]))

# Q1.2: fit log2(time) against k. A straight line means exponential growth
# in k; for comparison, also fit the sub-exponential L_N[1/2] shape that
# MPQS follows: time ~ exp(c * sqrt(ln N * ln ln N)).
xs = [RR(k) for k in KS]
ys = [log(results[k], 2).n() for k in KS]
n = len(xs)
mx, my = sum(xs) / n, sum(ys) / n
slope = sum((x - mx) * (y - my) for x, y in zip(xs, ys)) \
    / sum((x - mx)^2 for x in xs)
print("log2(time) grows by %.3f per bit: time doubles every %.1f bits"
      % (slope, 1 / slope))


def L(k):
    lnN = k * log(2.0)
    return exp(sqrt(lnN * log(lnN)))


c = sum(results[k] / L(k) for k in KS) / n
age_universe = 4.35e17  # seconds (13.8 billion years)
for k in [512, 1024, 2048]:
    t_lin = 2^(my + slope * (k - mx))
    t_L = c * L(k)
    print("k = %4d: exponential fit %.2e s, L[1/2] fit %.2e s"
          " (%.1e x age of the universe)" % (k, t_lin, t_L,
                                            t_L / age_universe))
