# Using RSA properly

`ex5.py` creates a 2048-bit key pair (`priv.pem`, `pub.pem`), encrypts with
RSA-OAEP and signs with RSA-PSS, using SHA-256 everywhere. It also writes
`c.bin`, `msg.txt` and `sig.bin` for the OpenSSL commands.

## Q5.1: Encrypt the same message twice with OAEP. Compare with Q3.1.

```
c1 = 1bb087af3377a473fe61619da31a07a5cf4e8e7ea962ba6e...
c2 = 3d79f830e64dcf170e8b6a625b4caa19b02ed4c9928466d6...
c1 == c2: False
```

The two ciphertexts are different, but both decrypt to the same message. OAEP
adds a random seed before applying RSA, so encryption is randomized. In Q3.1,
textbook RSA gave the same ciphertext twice, which broke IND-CPA; OAEP fixes
this.

## Q5.2: Try to encrypt a 256-byte message with OAEP under the 2048-bit key. What is the largest message that works, and where does that number come from?

A 256-byte message fails (`Encryption/decryption failed`). The largest message
that works is **190 bytes**.

OAEP needs room for its padding inside the 256-byte modulus: two hash
outputs (the seed and the label hash) and 2 extra bytes. With SHA-256
($h = 32$ bytes):

$$
256 - 2 \cdot 32 - 2 = 190 \text{ bytes}
$$

## Q5.3: Write an OAEP ciphertext to `c.bin` and decrypt it with OpenSSL. This fails. Why? Find OpenSSL's defaults for the OAEP hash and the mask generation function and fix the command.

It fails with `oaep decoding error` because the hashes don't match. Python
used SHA-256, but OpenSSL's default OAEP hash is **SHA-1**, and the MGF1 hash
defaults to the same as the OAEP hash (so also SHA-1).

Fixed command:

```
$ openssl pkeyutl -decrypt -inkey priv.pem -in c.bin \
    -pkeyopt rsa_padding_mode:oaep \
    -pkeyopt rsa_oaep_md:sha256 -pkeyopt rsa_mgf1_md:sha256
hello from python
```

## Q5.4: Sign a file with PSS in Python, write the signature to `sig.bin`, and verify it with OpenSSL. Then change one byte of `msg.txt` and verify again.

```
$ openssl dgst -sha256 -verify pub.pem -sigopt rsa_padding_mode:pss \
    -signature sig.bin msg.txt
Verified OK
```

After changing one byte of `msg.txt` (`I owe Alice 10 euros.` to
`I owe Alice 90 euros.`), the same command prints `Verification failure`.

Changing the message changes its SHA-256 hash, so the signature no longer
matches. The signature protects the integrity of the file.
