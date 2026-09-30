## Q2

**Yes, the encryption scheme is perfectly secure.**

The key has the same length as the message, and each component of the key is independently and uniformly selected from `{0, ..., 25}`.

Therefore, for any plaintext `m` and ciphertext `c` of length `n`, there exists exactly one key `k` such that `E(k, m) = c`.

Since all `26^n` keys are equally likely, observing the ciphertext does not reveal any additional information about the plaintext.

Thus, the scheme provides **perfect secrecy**.