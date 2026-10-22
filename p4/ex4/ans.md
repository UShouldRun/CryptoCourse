# Blocks vs Streams

One of the main distinguishing factors in real-world usage of symmetric
ciphers is the size of the ciphertext. Compare the ciphers explored this
week to those from the previous week.

## Q4.1: Compare the size of the plaintext with the size of the ciphertext produced in Q2 and Q3. What can you conclude?

In both Q2 and Q3 the ciphertext is exactly as long as the plaintext:

- Q2 (RC4): the 6-byte plaintext `secret` produced the 6-byte
  ciphertext `dfa520afd732` (12 hex chars).
- Q3 (ChaCha20): the 44-byte plaintext produced a 44-byte ciphertext
  (`od` offset `00002c`).

Conclusion: stream ciphers XOR the plaintext with a keystream of exactly
the same length, so no padding is needed and the ciphertext is never
longer than the plaintext.

## Q4.2: How do these differ from the AES-CTR and AES-CBC modes studied in the previous week?

- AES-CTR behaves like a stream cipher: AES generates keystream blocks
  from a nonce and a counter, and the plaintext is XORed with them. As
  with RC4 and ChaCha20 there is no padding and the ciphertext is the
  same length as the plaintext. The difference is that the keystream
  comes from a block cipher in counter mode rather than from a
  dedicated stream cipher.

- AES-CBC is a true block mode: it only processes full 16-byte blocks,
  so the plaintext must be padded (PKCS7) up to a multiple of 16. The
  ciphertext is therefore `ceil(len/16) * 16` bytes, up to 16 bytes
  longer than the plaintext, it is exactly 16 bytes longer whenever
  the plaintext is already a multiple of 16. The run from last week
  shows this: the 1710-byte `original.txt` produced a 1712-byte
  ciphertext. The keystream of Q2/Q3-style ciphers has no such block
  boundary.
