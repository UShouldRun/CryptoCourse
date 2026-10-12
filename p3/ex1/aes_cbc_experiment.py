import os
import subprocess

from pathlib import Path
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding


OUTPUT_DIR = Path("outputs")
OUTPUT_DIR.mkdir(exist_ok=True)

BLOCK_SIZE = 16  # AES block size in bytes


# ---------------------------------------------------
# Create original plaintext (at least 1000 bytes)
# ---------------------------------------------------

def create_plaintext():
    phrase = (
        "This is my cryptography experiment using AES-CBC. "
        "I want to verify that encryption and decryption work correctly.\n"
    )

    content = phrase * 15

    plaintext = content.encode("utf-8")

    assert len(plaintext) >= 1000

    (OUTPUT_DIR / "original.txt").write_bytes(plaintext)

    print(f"Original file created: {len(plaintext)} bytes")

    return plaintext


# ---------------------------------------------------
# PKCS7 padding helpers
# ---------------------------------------------------

def pad(data):
    padder = padding.PKCS7(128).padder()
    return padder.update(data) + padder.finalize()


def unpad(data):
    unpadder = padding.PKCS7(128).unpadder()
    return unpadder.update(data) + unpadder.finalize()


# ---------------------------------------------------
# AES-CBC encryption / decryption
# ---------------------------------------------------

def encrypt_aes_cbc(plaintext, key, iv):
    cipher = Cipher(
        algorithms.AES(key),
        modes.CBC(iv)
    )

    encryptor = cipher.encryptor()

    return encryptor.update(pad(plaintext)) + encryptor.finalize()


def decrypt_aes_cbc(ciphertext, key, iv):
    cipher = Cipher(
        algorithms.AES(key),
        modes.CBC(iv)
    )

    decryptor = cipher.decryptor()

    padded_plaintext = (
        decryptor.update(ciphertext) + decryptor.finalize()
    )

    return unpad(padded_plaintext)


# ---------------------------------------------------
# Modify exactly one ciphertext byte
# ---------------------------------------------------

def tamper_ciphertext(ciphertext):
    modified = bytearray(ciphertext)

    # Modify byte 32, which belongs to ciphertext block 3
    byte_index = 32

    modified[byte_index] ^= 0x01

    return bytes(modified)


# ---------------------------------------------------
# Q1.1 - Python cryptography
# ---------------------------------------------------

def question_1_1(plaintext, key, iv):

    print("\n--- Q1.1: Python AES-CBC ---")

    encrypted = encrypt_aes_cbc(plaintext, key, iv)

    (OUTPUT_DIR / "python_encrypted.bin").write_bytes(encrypted)

    decrypted = decrypt_aes_cbc(encrypted, key, iv)

    (OUTPUT_DIR / "python_decrypted.txt").write_bytes(decrypted)

    print("Decryption successful:", plaintext == decrypted)

    # Tampering experiment
    tampered = tamper_ciphertext(encrypted)

    (OUTPUT_DIR / "python_tampered.bin").write_bytes(tampered)

    tampered_decrypted = decrypt_aes_cbc(tampered, key, iv)

    (OUTPUT_DIR / "python_tampered.txt").write_bytes(
        tampered_decrypted
    )

    print("Tampered plaintext equals original:",
          plaintext == tampered_decrypted)


# ---------------------------------------------------
# Q1.2 - OpenSSL
# ---------------------------------------------------

def question_1_2(plaintext, key, iv):

    print("\n--- Q1.2: OpenSSL AES-CBC ---")

    original_path = OUTPUT_DIR / "original.txt"
    encrypted_path = OUTPUT_DIR / "openssl_encrypted.bin"
    decrypted_path = OUTPUT_DIR / "openssl_decrypted.txt"

    key_hex = key.hex()
    iv_hex = iv.hex()

    # Encrypt
    subprocess.run([
        "openssl", "enc",
        "-aes-256-cbc",
        "-e",
        "-in", str(original_path),
        "-out", str(encrypted_path),
        "-K", key_hex,
        "-iv", iv_hex
    ], check=True)

    # Decrypt
    subprocess.run([
        "openssl", "enc",
        "-aes-256-cbc",
        "-d",
        "-in", str(encrypted_path),
        "-out", str(decrypted_path),
        "-K", key_hex,
        "-iv", iv_hex
    ], check=True)

    decrypted = decrypted_path.read_bytes()

    print("Decryption successful:", plaintext == decrypted)

    # Tampering experiment
    encrypted = encrypted_path.read_bytes()

    tampered = tamper_ciphertext(encrypted)

    tampered_path = OUTPUT_DIR / "openssl_tampered.bin"
    tampered_path.write_bytes(tampered)

    subprocess.run([
        "openssl", "enc",
        "-aes-256-cbc",
        "-d",
        "-in", str(tampered_path),
        "-out", str(OUTPUT_DIR / "openssl_tampered.txt"),
        "-K", key_hex,
        "-iv", iv_hex
    ], check=True)

    tampered_decrypted = (
        OUTPUT_DIR / "openssl_tampered.txt"
    ).read_bytes()

    print("Tampered plaintext equals original:",
          plaintext == tampered_decrypted)


# ---------------------------------------------------
# Main
# ---------------------------------------------------

def main():

    plaintext = create_plaintext()

    # AES-256 key: 32 bytes
    key = os.urandom(32)

    # CBC IV: 16 bytes
    iv = os.urandom(16)

    question_1_1(plaintext, key, iv)
    question_1_2(plaintext, key, iv)

    print("\nExperiment completed. Check the outputs directory.")


if __name__ == "__main__":
    main()