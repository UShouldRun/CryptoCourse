
## Q5 — Length Extension Attack

### Objective

Demonstrate a length extension attack against an insecure message authentication scheme based on SHA-256.

The legitimate application computes:

`h = SHA256(k || m)`

where `k` is a secret key and `m` is the original message.

The attacker's objective is to construct a different message `m'` and a valid digest `h'`, without knowing the secret key.

### How the attack works

SHA-256 uses the Merkle–Damgård construction, which processes messages in blocks and maintains an internal hash state.

The final digest reveals the internal state after processing the original message and its padding.

An attacker who knows the original message, its digest, and the length of the secret key can use that digest as the starting state for additional hashing.

The forged message is constructed as:

`m' = m || padding || additional_data`

The attacker then calculates a new digest by continuing the SHA-256 computation from the original digest.

As a result:

`SHA256(k || m') = h'`

even though the attacker does not know `k`.

### Implementation

The demonstration uses two independent Python programs:

1. `legitimate.py` generates a random secret key, calculates the original SHA-256 digest, and saves the key, message, and digest into separate files.

2. `attacker.py` reads only the original message and digest, constructs the SHA-256 padding, and generates a forged message and digest.

The attacker assumes the secret key length is known. In a real attack, the key length could be guessed.

### Conclusion

The length extension attack demonstrates that using `SHA256(k || m)` directly as a message authentication code is insecure.

An attacker can generate a valid digest for an extended message without knowing the secret key.

The recommended solution is to use HMAC-SHA256, which is designed to prevent this type of attack.
