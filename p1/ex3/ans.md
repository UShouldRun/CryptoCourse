# Secret Sharing

Secret sharing is a method for distributing a secret by breaking
it into shares, which are distributed over multiple participants.
This is done in such a way that no individual holds enough
information about the secret to recover it, but such that when a
threshold of participants in the group combine their information,
the secret can be retrieved. There are somewhat complex ways to
do secret sharing, by representing the secret as points in a
polynomial, and using polynomial interpolation to reconstruct it,
also known as Shamir Secret Sharing. These are important building
blocks for an area of advanced cryptography: secure computation.

We will now consider a much simpler way to do it, which is to use
something that cryptographers love: the XOR ($`\oplus`$). To
exemplify how this can be done, let's do it such that message $`m`$
is broken into shares $`m_1, m_2, m_3`$, and can only be recovered if
all shares are gathered.

* $`m_1 \leftarrow_{\$} \{0, 1\}^n`$
* $`m_2 \leftarrow_{\$} \{0, 1\}^n`$
* $`m_3 \leftarrow m \oplus m_1 \oplus m_2`$

Observe that, without knowledge of all secrets, all possible
values of $`m`$ are equally probable. However, when all secrets are
combined, we can compute $`m = m_1 \oplus m_2 \oplus m_3`$ and
recover the message.

This will be used to distribute a message $`m \in \{0, 1\}^n`$,
divided into six secrets, and distributed over three participants
$`P_1, \dots, P_3`$, such that no two participants can recover the
message, but all three participants should be able to recover the
message.

* $`P_1: (m_1, m_2)`$
* $`P_2: (m_3, m_4)`$
* $`P_3: ?`$

The following are alternatives of shares to be given to $`P_3`$:

1. $`(m_5, m_6)`$
2. $`(m_3, m_4, m_5, m_6)`$
3. $`(m_2, m_3, m_5, m_6)`$
4. $`(m_1, m_4, m_5)`$

---

### Questions

* **Q3.1:** Explain which of the proposed alternatives meets the
  aforementioned criteria.

  The correct alternative is number 1. With the combined 6 parts,
  $`m`$, which is defined by $`m \leftarrow m_1 \oplus \dots \oplus m_6`$,
  the 3 participants can recover the original message by combining the
  6 secrets. With number 2, participant 3 would have too much information
  and would be able to recover the original message with just participant
  number 1, making it possible for 2 participants to recover the message.
  Alternative number 3 makes it so they have to be all together, because,
  even with more information, there is 1 secret, $`m_1`$ and $`m_4`$, with
  participant number 1 and number 2, respectively. However, if for some
  reason one of them gets one of the remaining secrets, it would break the
  criteria. So, alternative number 1 is more desirable. Alternative number 4
  does not work, because the sixth secret is not shared with any of the
  participants, making it impossible to recover the original message.

* **Q3.2:** Propose an alternative distribution of these six
  secrets over the same three participants, in a way that now
  allows for any two participants to recover the message, but no
  single participant to recover it.

```math
  m \leftarrow (m_1 \oplus m_2) \oplus (m_3 \oplus m_4) \oplus (m_5 \oplus m_6)
```

```math
  m_k \leftarrow_{\$} \{0, 1\}^n, \quad \forall k \in \{1, \dots, 5\}
```

```math
  m_6 \leftarrow m \oplus m_1 \oplus \dots \oplus m_5
```

  * $`P_1: (m_1, m_2, m_3, m_4)`$
  * $`P_2: (m_3, m_4, m_5, m_6)`$
  * $`P_3: (m_1, m_2, m_5, m_6)`$

* **Q3.3:** Suppose you use this scheme to secret share two
  values $`x = 001`$ and $`y = 010`$. Experiment generating three
  shares $`x_0, x_1, x_2`$ that reconstruct to $`001`$ and three
  shares $`y_0, y_1, y_2`$ that reconstruct to $`010`$. What happens
  if you now do $`x_0 \oplus y_0`$, $`x_1 \oplus y_1`$ and
  $`x_2 \oplus y_2`$? What is the relation of the resulting
  reconstructing value to $`x`$ and $`y`$?

```math
  x_k \leftarrow_{\$} \{0, 1\}^n, \quad \forall k \in \{1, 2\}
```

```math
  x_0 \leftarrow x \oplus x_1 \oplus x_2
```

  Let $`x_1 := 111`$ and $`x_2 := 101`$, then

```math
  x_0 = 001 \oplus 111 \oplus 101 = 110 \oplus 101 = 011
```

```math
  y_k \leftarrow_{\$} \{0, 1\}^n, \quad \forall k \in \{1, 2\}
```

```math
  y_0 \leftarrow y \oplus y_1 \oplus y_2
```

  Let $`y_1 := 011`$ and $`y_2 := 100`$, then

```math
  y_0 = 010 \oplus 011 \oplus 100 = 001 \oplus 100 = 101
```

  If we know $`z_0 := x_0 \oplus y_0`$, $`z_1 := x_1 \oplus y_1`$
  and $`z_2 := x_2 \oplus y_2`$, then we know $`z = x \oplus y`$.
  Let $`z := z_0 \oplus z_1 \oplus z_2`$; because XOR is commutative
  and associative:

```math
  \begin{aligned}
  z &= z_0 \oplus z_1 \oplus z_2 \\
    &= x_0 \oplus y_0 \oplus x_1 \oplus y_1 \oplus x_2 \oplus y_2 \\
    &= (x_0 \oplus x_1 \oplus x_2) \oplus (y_0 \oplus y_1 \oplus y_2) \\
    &= x \oplus y
  \end{aligned}
```
