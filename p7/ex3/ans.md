# Textbook RSA is not a secure public key encryption (PKE) scheme

Think of `eval` as given as encryption, taking a public key and a message and
returning a ciphertext. Similarly, think of `inv` as given as decryption.

## Q3.1: Call `eval` twice on the same message. What do you observe, and which security notion for PKE does this violate?

Calling `eval` twice on the same message `attack at dawn` gives the same
ciphertext both times:

```
c1 = 5a9304dd637e0436f59b532ee663df48ed73c2210480ce19...
c2 = 5a9304dd637e0436f59b532ee663df48ed73c2210480ce19...
c1 == c2: True
```

The algorithm is deterministic: $c = m^e \bmod n$ depends only on $m$, $e$
and $n$, so the same message always gives the same ciphertext.

This violates **IND-CPA**. The attacker chooses two messages $m_0, m_1$ and
receives the challenge $c = eval(m_b)$. It can compute $m_0^e \bmod n$
itself; if this equals $c$ it returns $0$, otherwise $1$. It wins with
probability 1, so its advantage is $\frac{1}{2}$.

In public key encryption the attacker doesn't even need an encryption
oracle, because the public key lets anyone encrypt. That is why no
deterministic PKE scheme can be IND-CPA secure.

## Q3.2: Take $c \leftarrow eval(m)$. Without using the private key, produce a ciphertext $c'$ such that $inv(c')$ recovers $2m$. Why is this a problem for public key encryption applications?

The ciphertext of $2m$ can be written in terms of $c$:

$$
(2m)^e \bmod n = (2^e \cdot m^e) \bmod n = (2^e \cdot c) \bmod n
$$

So $c' = (2^e \cdot c) \bmod n$, computed with the public key $(n, e)$
only. Tested with $m = 100$: $inv(c')$ returned $200$.

This property is called **malleability**, and it is a problem for two
reasons:

- **Integrity.** Even though an attacker may not know the content of the
  message, without a way to verify the authenticity of the message it can
  change it like this (for example, doubling an encrypted payment amount),
  and the receiver will not know it.
- **Confidentiality.** Textbook RSA is not **IND-CCA** secure. In the IND-CCA
  game the attacker cannot decrypt the challenge $c$ itself, but it can query
  $inv((2^e \cdot c) \bmod n)$, get $2m_b$, divide by 2, and learn $m_b$.
  This is the idea behind Bleichenbacher's attack on RSA in TLS (1998, and
  again as ROBOT in 2017): the server's padding errors acted as a partial
  decryption oracle.

The fix is to use padding such as **RSA-OAEP**, which randomizes the message
and destroys the multiplicative structure, making the scheme IND-CCA secure.
