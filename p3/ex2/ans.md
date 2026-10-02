**Q2.1**

If we modify the first byte of the second block in the ciphertext, all following blocks will be wrong in the plaintext, so blocks 2,3,4. This is because when decrypting, the ciphered block *X* needs the block *X - 1* to be decrypted, so 4 needs 3 and 3 needs 2. Since 2 is broken, all the others will be too.


**Q2.2**

If AES-CTR is used, only the block 2 will be different, because in this implementation, every block is independent from eachother.

**Q2.3**

(Assuming the changed bytes are all in the same block)

Yes, we can just modify the single block since every block is independent and the change is in the same number of bytes (3).

In this case you would only need to calculate which *nonce+counter* would be used in the encryption, according to the number of the block.

**2.4**

Again, this could not be done, because changing a block changes all subsequent blocks. You would need to encrypt/decrypt all blocks after and including the changed block.