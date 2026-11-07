"""Q5: RSA-OAEP encryption and RSA-PSS signatures with one key pair (SHA-256).

Run from this folder:  python3 ex5.py
Writes priv.pem, pub.pem, c.bin, msg.txt and sig.bin for the OpenSSL commands.
"""

from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding, rsa

key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
pub = key.public_key()

with open("priv.pem", "wb") as f:
    f.write(key.private_bytes(serialization.Encoding.PEM,
                              serialization.PrivateFormat.PKCS8,
                              serialization.NoEncryption()))
with open("pub.pem", "wb") as f:
    f.write(pub.public_bytes(serialization.Encoding.PEM,
                             serialization.PublicFormat.SubjectPublicKeyInfo))

oaep = padding.OAEP(mgf=padding.MGF1(hashes.SHA256()),
                    algorithm=hashes.SHA256(), label=None)
pss = padding.PSS(mgf=padding.MGF1(hashes.SHA256()),
                  salt_length=padding.PSS.MAX_LENGTH)

# Q5.1: encrypt the same message twice
msg = b"attack at dawn"
c1, c2 = pub.encrypt(msg, oaep), pub.encrypt(msg, oaep)
print("Q5.1")
print("  c1 =", c1.hex()[:48] + "...")
print("  c2 =", c2.hex()[:48] + "...")
print("  c1 == c2:", c1 == c2)
print("  both decrypt to the message:",
      key.decrypt(c1, oaep) == key.decrypt(c2, oaep) == msg)

# Q5.2: largest message OAEP accepts under a 2048-bit key
print("Q5.2")
try:
    pub.encrypt(b"A" * 256, oaep)
except ValueError as err:
    print("  256 bytes:", err)
largest = None
for n in range(256, 0, -1):
    try:
        pub.encrypt(b"A" * n, oaep)
        largest = n
        break
    except ValueError:
        pass
print("  largest message that works:", largest, "bytes")

# Q5.3: OAEP ciphertext for OpenSSL
with open("c.bin", "wb") as f:
    f.write(pub.encrypt(b"hello from python\n", oaep))

# Q5.4: PSS signature on msg.txt
with open("msg.txt", "wb") as f:
    f.write(b"I owe Alice 10 euros.\n")
with open("msg.txt", "rb") as f:
    sig = key.sign(f.read(), pss, hashes.SHA256())
with open("sig.bin", "wb") as f:
    f.write(sig)
print("Wrote priv.pem, pub.pem, c.bin, msg.txt, sig.bin")
