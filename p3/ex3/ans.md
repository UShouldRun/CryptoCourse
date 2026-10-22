# Q3: IND-CPA secure schemes

Consider a one-time IND-CPA secure encryption scheme
$(E, D)$, with message and ciphertext space
$\{0, 1\}^n$. We now want to propose an alternative
encryption scheme $(E', D')$, which will be built from
$(E, D)$. Consider the following alternatives:

| # | $E'(k, m)$ | $D'(k, c)$ |
|---|------------|------------|
| 1 | $\text{reverse}(E(k,m))$ | $\text{reverse}(D(k,c))$ |
| 2 | $E(0^n, m)$ | $D(0^n, c)$ |
| 3 | $E(k, m) \|\| 0$ | $D(k, c[0..n])$ |
| 4 | $E(k, m) \oplus 1^n$ | $D(k, (c \oplus 1^n))$ |
| 5 | $E(k, 0^n)$ | $D(k, 0^n)$ |
| 6 | $E(k, m) \|\| m$ | $D(k, c[0..n])$ |

## Q3.1: Which of the encryption schemes $E'$ are correct $\forall m, k, D'(k, E'(k, m)) = m$?

1. $E'(k, m) = \text{reverse}(E(k, m))$;
   $D'(k, c) = \text{reverse}(D(k, c))$

$$
\forall m, k: \; D'(k, E'(k, m)) = \text{reverse}(D(k, \text{reverse}(E(k, m))))
$$

In general, $\text{reverse}(E(k, m))$ is not a valid
ciphertext of any message, so feeding it to $D$ yields a
result unrelated to $m$, and the outer $\text{reverse}$
does not fix it. For this scheme to be correct, we would
either need

$$
E'(k, m) = \text{reverse}(E(k, m)) \\
D'(k, c) = D(k, \text{reverse}(c))
$$

which results in
$$
\begin{aligned}
\forall m, k: \quad D'(k, E'(k, m)) &= D(k, \text{reverse}(\text{reverse}(E(k, m)))) \\
                                    &= D(k, E(k, m)) \\
                                    &= m
\end{aligned}
$$

or

$$
E'(k, m) = E(k, \text{reverse}(m)) \\
D'(k, c) = \text{reverse}(D(k, c))
$$

which results in
$$
\begin{aligned}
\forall m, k: \quad D'(k, E'(k, m)) &= \text{reverse}(D(k, E(k, \text{reverse}(m)))) \\
                                    &= \text{reverse}(\text{reverse}(m)) \\
                                    &= m
\end{aligned}
$$

2. $E(0^n, m); D(0^n, c)$

Is correct, as

$$
\forall m, k: \; D'(k, E'(k, m)) \;=\; D(0^n, E(0^n, m)) \;=\; m
$$

3. $E(k, m) \mathbin{\|\|} 0; D(k, c[0..n])$

Is correct, as

$$
\begin{aligned}
\forall m, k: \quad D'(k, E'(k, m)) &= D(k, (E(k, m) \mathbin{\|\|} 0)[0..n]) \\
                                    &= D(k, E(k, m)) \\
                                    &= m
\end{aligned}
$$

4. $E(k, m) \oplus 1^n; D(k, (c \oplus 1^n))$

Is correct, as

$$
\begin{aligned}
\forall m, k: \quad D'(k, E'(k, m)) &= D(k, (E(k, m) \oplus 1^n) \oplus 1^n) \\
                                    &= D(k, E(k, m) \oplus (1^n \oplus 1^n)) \\
                                    &= D(k, E(k, m) \oplus 0^n) \\
                                    &= D(k, E(k, m)) \\
                                    &= m
\end{aligned}
$$

5. $E(k, 0^n); D(k, 0^n)$

Is incorrect, as

$$
\forall m, k: \; D'(k, E'(k, m)) \;=\; D(k, 0^n) \;=\; m^*
$$

for some fixed message $m^* = D(k, 0^n)$, independent of the
plaintext actually encrypted. So correctness holds only for
$m = m^*$, not for all $m$; in particular, for any
$m \neq m^*$ we have $D'(k, E'(k, m)) = m^* \neq m$.

6. $E(k, m) \mathbin{||} m; D(k, c[0..n])$

Is correct, as

$$
\begin{aligned}
\forall m, k: \quad D'(k, E'(k, m)) &= D(k, (E(k, m) \mathbin{||} m)[0..n]) \\
                                    &= D(k, E(k, m)) \\
                                    &= m
\end{aligned}
$$

## Q3.2: Which of the correct encryption schemes $E'$ are also (one-time) IND-CPA secure?

- 2: Is not IND-CPA secure, as the encryption key is not
sampled at all: it is fixed to $0^n$, so encryption under
it is a public deterministic function of $m$, and an
adversary can distinguish by simply checking whether the
challenger's ciphertext equals $E(0^n, m)$ for its chosen
messages.

- 3: Is IND-CPA secure, as it does not undermine the sampling
of the encryption key or give to an attacker any information
about the plaintext or the key.

- 4: Is IND-CPA secure, as it does not undermine the sampling
of the encryption key or give to an attacker any information
about the plaintext or the key.

- 6: Is not IND-CPA secure, as it appends the actual plaintext
to the encrypted ciphertext.

## Q3.3: Recall the one-time IND-CPA experiment. Select one of the correct, but insecure schemes, and describe how an attacker can break the security model.

Let's choose scheme number 6. In the one-time IND-CPA
experiment, the attacker picks two distinct messages
$m_0, m_1 \in \{0, 1\}^n$, the challenger flips a uniform
bit $b$ and gives the attacker $c' = E'(k, m_b)$, and the
attacker must output a guess $b'$ of $b$.

Since $E'(k, m) = E(k, m) \mathbin{||} m$, the challenge
ciphertext is

$$
c' = E(k, m_b) \mathbin{||} m_b
$$

so its last $n$ bits are exactly the plaintext $m_b$. The
attacker simply compares these last $n$ bits to $m_0$ and
$m_1$, and outputs

$$
b' = \begin{cases} 0 & \text{if } m_b = m_0 \\ 1 & \text{if } m_b = m_1 \end{cases}
$$

It wins with probability $1$, so its advantage is

$$
\left| \Pr[b' = b] - \tfrac{1}{2} \right| = \tfrac{1}{2}
$$

which is not negligible, hence scheme 6 is not IND-CPA
secure. Notice that no key recovery is needed: the
plaintext is transmitted in the clear next to the
ciphertext, so the attacker can perfectly distinguish the
two possible challenge messages.
