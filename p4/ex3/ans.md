# Repetitive effort

## Q3.1: Produce a small script that demonstrates with OpenSSL that ChaCha20 produces a repeated ciphertext if you encrypt the same file with the same key and nonce.

Answered with `chacha20_repeat.sh`.

## Q3.2: Explain why this is the case.

ChaCha20 is a stream cipher: it generates a keystream from the key
and nonce, then XORs it with the plaintext — `C = P XOR S(key,
nonce)`. The keystream never depends on the plaintext, so the same
key and nonce always produce the same `S`, and the same file always
XORs to the same `C`. There is no per-run randomness in the
algorithm; the nonce is the only thing that varies the keystream,
which is why a fresh nonce changes the output.
