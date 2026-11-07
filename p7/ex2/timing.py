"""Q2.2: time keygen, eval and inv from RSA.py for 2048- and 4096-bit keys.

Run from this folder:  python3 timing.py
"""

import os
import sys
import time

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "code"))
import RSA  # noqa: E402

RUNS = {"keygen": 10, "eval": 1000, "inv": 100}


def mean_time(fn, runs):
    start = time.perf_counter()
    for _ in range(runs):
        fn()
    return (time.perf_counter() - start) / runs


for bits in (2048, 4096):
    pub_pem, priv_pem = RSA.keygen(bits)
    pk, sk = RSA.load_pub(pub_pem), RSA.load_priv(priv_pem)
    m = os.urandom(bits // 8 - 1)  # random message, smaller than n
    c = RSA.eval(pk, m)
    assert RSA.inv(sk, c).lstrip(b"\0") == m.lstrip(b"\0")

    t_keygen = mean_time(lambda: RSA.keygen(bits), RUNS["keygen"])
    t_eval = mean_time(lambda: RSA.eval(pk, m), RUNS["eval"])
    t_inv = mean_time(lambda: RSA.inv(sk, c), RUNS["inv"])

    e, d = pk[1], sk[1]
    print(f"{bits}-bit key: e has {e.bit_length()} bits "
          f"({bin(e).count('1')} ones), d has {d.bit_length()} bits "
          f"({bin(d).count('1')} ones)")
    print(f"  keygen {t_keygen * 1e3:9.3f} ms")
    print(f"  eval   {t_eval * 1e3:9.3f} ms")
    print(f"  inv    {t_inv * 1e3:9.3f} ms   (inv/eval = {t_inv / t_eval:.0f}x)")
