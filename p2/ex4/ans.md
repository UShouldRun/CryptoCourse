# Key Generation

Tested with OpenSSL 3.0.13. Times vary between machines
and runs.

## Q4.1 — RSA key pair

```bash
# Generate a key pair
openssl genpkey -algorithm RSA -pkeyopt rsa_keygen_bits:2048 -out rsa.pem

# Extract the public key
openssl pkey -in rsa.pem -pubout -out rsa_pub.pem

# See what's inside
openssl pkey -in rsa.pem -text -noout
```

The key contains the modulus n = p · q, the public
exponent e (65537), the private exponent d, the two
primes p and q, and some extra values used to speed up
computations.

| Key size (bits) | Time       | File size (bytes) |
|-----------------|------------|-------------------|
| 1024            | ~0.03 s    | 916               |
| 2048            | ~0.1 s     | 1704              |
| 3072            | ~0.6 s     | 2484              |
| 4096            | ~1 – 3 s   | 3272              |

**What happens when the size changes:**

- **Bigger keys take longer to generate.** OpenSSL has
  to find two large random primes, and bigger primes are
  rarer and slower to test.
- **The time varies between runs** because the primes
  are found by trying random numbers until one works.
- **Bigger keys are more secure.** 1024 bits is no
  longer safe; 2048 is the minimum today.
- **Keys that are too small are refused.** OpenSSL 3
  rejects anything below 512 bits.

## Q4.2 — Diffie-Hellman parameters

```bash
# Generate DH parameters
openssl genpkey -genparam -algorithm DH \
  -pkeyopt dh_paramgen_prime_len:2048 \
  -out dhparams.pem

# See what's inside
openssl pkeyparam -in dhparams.pem -text -noout

# Generate a DH key pair from those parameters
openssl genpkey -paramfile dhparams.pem -out dhkey.pem
```

The parameters are just two public numbers: a large
prime **p** and a generator **g** (usually 2).

| Prime size (bits) | Time           |
|-------------------|----------------|
| 512               | ~0.03 s        |
| 1024              | ~0.2 – 0.6 s   |
| 2048              | ~26 s          |

Generating a DH key pair from existing parameters took
only ~0.01 s.

## Conclusion

- **DH parameters take much longer to generate than RSA
  keys** (~26 s vs ~0.1 s at 2048 bits). DH needs a
  *safe prime* (p where (p − 1)/2 is also prime), which
  is much rarer than a normal prime.
- **But DH parameters are public and reusable.** They
  only need to be generated once and can be shared by
  everyone. Generating the actual DH keys is fast. In
  practice, standard pre-made parameters are often used.
- **RSA keys are faster to generate but must be kept
  secret**, and each user needs their own.
- **For both, bigger sizes mean more security but slower
  generation.**
