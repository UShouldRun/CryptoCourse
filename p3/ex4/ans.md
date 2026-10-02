**Q4**

The first thing to do is ask the oracle for the encryption of message *M*.

Since the IV is static, this means this is a deterministic encryption. The same message encrypted twice will produce the same result.

Now m0 will be *M* and m1 will be any other message. If the received encrypted message is the same as the one received in the oracle, we know b = 0, otherwise b = 1.