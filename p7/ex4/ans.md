# Textbook RSA is not a secure public key signature scheme

Think of `inv` as given as signing, taking a secret key and a message and
returning a signature. Similarly, think of `eval` as given as verification.

## Q4.1: Produce a valid signature for $m = 1$ without calling `inv`. Why is this a relevant attack for signature schemes?

$\sigma = 1$ is a valid signature for $m = 1$, because verification computes
$1^e \bmod N = 1$.

More generally, pick any $\sigma$ and set $m = \sigma^e \bmod N$; then
$(m, \sigma)$ is valid. This breaks **UF-CMA**: the attacker outputs a valid
signature on a new message using only the public key.

## Q4.2: Blinding. Pick a random $r$ and ask `inv` to sign $r^e \cdot m \bmod N$ instead of $m$. Show how to turn the result into a valid signature on $m$. Why is this a relevant attack for signature schemes?

$$
\sigma' = (r^e \cdot m)^d = r^{ed} \cdot m^d = r \cdot m^d \bmod N
$$

Multiplying by $r^{-1} \bmod N$ gives $\sigma = m^d \bmod N$, a valid
signature on $m$.

This is a problem because the signer only sees a random-looking number, so it
signs $m$ without knowing it. The attacker gets a signature on a message of
its choice that was never queried, which breaks **UF-CMA**.

## Q4.3: Would any of the above attacks work if signing computes $inv(H(m))$ instead of $inv(m)$, for a cryptographic hash function $H$? Investigate whether the resulting signature scheme is secure.

No. Now $\sigma = H(m)^d \bmod N$, and each attack needs to break the hash:

- **Q4.1:** needs an $m$ with $H(m) = \sigma^e \bmod N$, a preimage.
- **Q4.2:** needs an $x$ with $H(x) = r^e \cdot H(m)$, a preimage.
- **Collision:** if $H(m_1) = H(m_2)$, a signature on $m_1$ is also valid for
  $m_2$, which collision resistance prevents.

This scheme is RSA-FDH, and it is provably secure (UF-CMA) in the Random Oracle
Model. In practice RSA-PSS (FDH with a random salt) is recommended.
