### Q1.3 — Informally describe what happened

After modifying a single byte of the ciphertext and decrypting it again, the resulting plaintext was partially corrupted.

Since AES-CBC operates on 16-byte blocks, modifying one byte in a ciphertext block affects two plaintext blocks during decryption:

- **The corresponding plaintext block** becomes corrupted due to the avalanche effect of AES.
- **The following plaintext block** has exactly one bit flipped at the corresponding position.
- **All remaining plaintext blocks** are unaffected.

Despite the modification, decryption completed successfully because AES-CBC does not provide integrity protection or authentication.

This experiment demonstrates that **AES-CBC provides confidentiality but does not guarantee data integrity**. A modified ciphertext can still be decrypted without producing an error, even though the resulting plaintext differs from the original.