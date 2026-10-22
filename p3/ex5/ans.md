# Q5: Not-quite-so-unpredictable Initialization Vectors

Nonce-based encryption schemes are encryption schemes
that take the nonce as a parameter.

$Enc(k, m, n)$ takes key $k$, message $m$ and nonce $n$.

These are secure, as long as no nonce is ever used
twice. E.g. AES-CTR is a nonce-based encryption scheme.

Consider the following encryption scheme:

- Use the block encryption function (with the same key)
  on the nonce to generate an IV, $IV \leftarrow E(k, n)$

- Compute the encryption of the message using AES-CBC
  with IV

Observe that this prevents trivial attacks, such as
setting the IV to $0$ – as it is encrypted – and also
disallows fixing the IV – as the same nonce cannot be
reused. However, the IV is predictable, and that can lead
to an attack.

## Q5.1: Construct an attack against the nonce-based IND-CPA security experiment of this scheme.

In the nonce-based IND-CPA experiment, the attacker
picks two messages $m_0, m_1$ and a nonce $n$, the
challenger flips a uniform bit $b$ and returns
$c^* = Enc(k, m_b, n)$, and the attacker must output a
guess $b'$ of $b$, with access to an encryption oracle
for the same scheme under the same key.

Take $n = 0^l$ and $m_0 = 0^l$, with $l$ the size of a
block (16 bytes), and let $m_1 \neq m_0$ be any other
message of the same size. The challenge ciphertext is

$$
\begin{aligned}
c^* &= Enc(k, m_b, 0^l) \\
    &= \text{AES-CBC}_k(m_b; \ IV = E(k, 0^l))
\end{aligned}
$$

Since the first block of $m_0$ is all zeros, its first
ciphertext block is

$$
c^*_0 = E(k, IV \oplus 0^{128}) = E(k, E(k, 0^l))
$$

Now the "correlated" query: ask the encryption oracle to
encrypt $m_0$ under a fresh nonce $n' = 0^l$, i.e.
request $c' = Enc(k, m_0, 0^l) = Enc(k, 0^l, 0^l)$. By
the scheme's construction, this oracle encryption has
the same IV, $IV = E(k, 0^l)$, so its first block is

$$
c'_0 = E(k, E(k, 0^l)) = c^*_0
$$

So the oracle's output is a correlated encryption whose
first block is identical to the first block of the
challenge ciphertext, and this can only happen if the
challenge message was $m_0$ (the IV is a pseudorandom
block, so the probability that $m_1$'s first ciphertext
block collides with it is negligible).

The attack:

1. Query the oracle: $c' \leftarrow Enc(k, m_0, 0^l)$
2. If $c^*_0 = c'_0$ (equivalently, $c^* = c'$, since
   $m_0$ is exactly one block), output $b' = 0$
3. Otherwise, output $b' = 1$

It wins with probability $1 - 2^{-128}$, so its
advantage is

$$
\left| \Pr[b' = b] - \tfrac{1}{2} \right| \approx \tfrac{1}{2}
$$

which is not negligible. The key insight from the hint:
encrypting $0^l$ under nonce $0^l$ gives the attacker
$E(k, E(k, 0^l))$, which is exactly the first ciphertext
block of $Enc(k, 0^l, 0^l)$ — a correlation with the
challenge that reveals whether $b = 0$.

## Q5.2: Write a program that prints the messages/ciphertexts used in this attack, and that shows this IND-breaking correlation.

See `attack.py`. It runs the attack against both values
of the hidden bit $b$: when $b = 0$ the challenge
ciphertext matches the oracle's correlated encryption,
and when $b = 1$ it does not.
