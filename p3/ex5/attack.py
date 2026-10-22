"""
Q5.2 - Attack on the nonce-based scheme:

    IV <- E(k, nonce)          (AES-128 on the nonce)
    c  <- AES-CBC_k(m, IV)     (PKCS7 padding)

Attack (from Q5.1): the attacker picks m0 = 0^l, m1 != m0
and the nonce n = 0^l, receives the challenge c* =
Enc(k, m_b, 0^l), then asks the encryption oracle for
c' = Enc(k, m0, 0^l). If the first ciphertext blocks of
c* and c' are equal, the attacker outputs b' = 0, else
b' = 1.
"""

import os

from cryptography.hazmat.primitives.ciphers import (
    Cipher,
    algorithms,
    modes
)
from cryptography.hazmat.primitives import padding

BLOCK_SIZE = 16  # AES block size, in bytes
NONCE = bytes(BLOCK_SIZE)  # n = 0^l

def hex_bytes(data):
    return data.hex()

def aes_encrypt_block(block, key):
    """E(k, x): single AES-128 block encryption."""
    cipher = Cipher(algorithms.AES(key), modes.ECB())
    encryptor = cipher.encryptor()
    return encryptor.update(block) + encryptor.finalize()

def generate_iv(key, nonce):
    """IV <- E(k, nonce)."""
    return aes_encrypt_block(nonce, key)

def pad(data):
    padder = padding.PKCS7(128).padder()
    return padder.update(data) + padder.finalize()

def aes_cbc_encrypt(message, key, iv):
    """AES-CBC encryption with PKCS7 padding."""
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
    encryptor = cipher.encryptor()
    return encryptor.update(pad(message)) + encryptor.finalize()

def enc(key, message, nonce):
    """The scheme: IV <- E(k, nonce); c <- AES-CBC_k(m, IV)."""
    iv = generate_iv(key, nonce)
    return iv, aes_cbc_encrypt(message, key, iv)

def attack(challenge_ct):
    """
    The attacker's decision rule.

    It holds a challenge ciphertext and access to an
    encryption oracle (same key). It outputs its guess
    b' in {0, 1}.
    """

    m0 = bytes(BLOCK_SIZE)
    _, oracle_ct = enc(KEY, m0, NONCE)

    if challenge_ct[0:16] == oracle_ct[0:16]:
        return 0
    else:
        return 1

def main():
    global KEY

    KEY = os.urandom(16)

    # Attacker's chosen messages
    m0 = bytes(BLOCK_SIZE)      # 0^l (per the hint)
    m1 = os.urandom(BLOCK_SIZE)  # anything != m0

    print("--- Q5.2: Nonce-based IND-CPA attack ---\n")

    print(f"key   k  = {hex_bytes(KEY)}")
    print(f"nonce n  = {hex_bytes(NONCE)}")
    print(f"message m0 = {hex_bytes(m0)}")
    print(f"message m1 = {hex_bytes(m1)}\n")

    iv = generate_iv(KEY, NONCE)
    print(f"IV = E(k, 0^l) = {hex_bytes(iv)}\n")

    for b in (0, 1):
        m_b = m0 if b == 0 else m1

        _, c_star = enc(KEY, m_b, NONCE)

        b_prime = attack(c_star)

        print(f"b = {b}:  challenge c* = Enc(k, m_b, 0^l)")
        print(f"          c* = {hex_bytes(c_star)}")

        _, c_oracle = enc(KEY, m0, NONCE)
        print(f"oracle query: c' = Enc(k, m0, 0^l)")
        print(f"          c' = {hex_bytes(c_oracle)}")

        print(f"first blocks: c*[0..16] = "
              f"{hex_bytes(c_star[0:16])}")
        print(f"               c'[0..16] = "
              f"{hex_bytes(c_oracle[0:16])}")

        correlated = c_star[0:16] == c_oracle[0:16]
        print(f"correlated? {correlated}")
        print(f"attacker outputs b' = {b_prime}"
              f"  ->  {'correct' if b_prime == b else 'wrong'}\n")

if __name__ == "__main__":
    main()
