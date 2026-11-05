
## Q4 — A SHAttering Realization

### Q4.1 — SHA-1 Collision

To demonstrate a SHA-1 collision, I used the two PDF files published by the SHAttered research team in 2017.

The files contain different data but produce exactly the same SHA-1 hash:

`38762cf7f55934b34d179ae6a4c80cadccbb7f0a`

The collision can be verified using OpenSSL:

```bash
openssl dgst -sha1 shattered-1.pdf
openssl dgst -sha1 shattered-2.pdf
```

Although their SHA-1 digests are identical, the files have different contents and produce different SHA-256 digests.

This demonstrates that SHA-1 is no longer collision resistant.

### Q4.2 — How the SHAttered Attack Works

The SHAttered attack, published in 2017 by researchers from Google and CWI Amsterdam, demonstrated the first practical collision against the full SHA-1 algorithm.

The researchers exploited weaknesses in SHA-1's compression function to construct two different sequences of message blocks that produce the same internal hash state.

By carefully controlling the differences between these blocks, they were able to make the differences cancel out during hash computation.

These specially constructed blocks were embedded into two PDF documents that display different content but produce the same SHA-1 hash.

The attack required approximately 2^63.1 SHA-1 compression operations, significantly less than the 2^80 operations expected from a generic birthday attack.

**Conclusion:** The SHAttered attack demonstrates that SHA-1 is vulnerable to practical collision attacks and should no longer be used in security applications that require collision resistance. Modern alternatives include SHA-256 and SHA-3.

### References

- SHAttered research paper: https://shattered.io/static/shattered.pdf
- PDF 1: https://shattered.io/static/shattered-1.pdf
- PDF 2: https://shattered.io/static/shattered-2.pdf
