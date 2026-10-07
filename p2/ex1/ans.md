### 1.1

Since $C$ is an 8-bit string, there are $2^8 = 256$ possible values, corresponding to the integers from $0$ to $255$.

The distribution is defined as:

$$
D(C) = C \bmod 251
$$

For example:

| $C$ | $D(C)$ | $S$ |
|---:|---:|---:|
| 0 | $0 \bmod 251 = 0$ | 0 |
| 1 | $1 \bmod 251 = 1$ | 1 |
| 2 | $2 \bmod 251 = 2$ | 2 |
| 3 | $3 \bmod 251 = 3$ | 3 |
| 4 | $4 \bmod 251 = 4$ | 4 |
| 5 | $5 \bmod 251 = 5$ | 5 |
| 6 | $6 \bmod 251 = 6$ | 6 |
| $\vdots$ | $\vdots$ | $\vdots$ |
| 251 | $251 \bmod 251 = 0$ | 0 |
| 252 | $252 \bmod 251 = 1$ | 1 |
| 253 | $253 \bmod 251 = 2$ | 2 |
| 254 | $254 \bmod 251 = 3$ | 3 |
| 255 | $255 \bmod 251 = 4$ | 4 |

Therefore, each value $S' \in \{0,1,2,3,4\}$ is produced by two different values of $C$, while each value $S' \in \{5,\ldots,250\}$ is produced by only one value of $C$.

Thus,

$$
\Pr[S=S'] =
\begin{cases}
\frac{2}{256}, & S' \in \{0,\ldots,4\} \\
\frac{1}{256}, & S' \in \{5,\ldots,250\}
\end{cases}
$$

### 1.2

Since $C$ is now a 64-bit string, there are $2^{64}$ possible values, corresponding to the integers from $0$ to $2^{64}-1$.

The distribution is still defined as:

$$
D(C) = C \bmod 251
$$

We have:

$$
2^{64} = 251 \times 73\,493\,004\,277\,727\,297 + 69
$$

Therefore, the values $S' \in \{0,\ldots,68\}$ are each produced by $73\,493\,004\,277\,727\,298$ different values of $C$.

The remaining values $S' \in \{69,\ldots,250\}$ are each produced by $73\,493\,004\,277\,727\,297$ different values of $C$.

Thus,

$$
\Pr[S=S'] =
\begin{cases}
\frac{73\,493\,004\,277\,727\,298}{2^{64}}, & S' \in \{0,\ldots,68\} \\[6pt]
\frac{73\,493\,004\,277\,727\,297}{2^{64}}, & S' \in \{69,\ldots,250\}
\end{cases}
$$

### 1.3

Neither distribution is uniform, since not all values in $S$ have the same probability of being produced.

Entropy can be used to quantify how close the distributions are to uniform. It is defined as:

$$
H(S) = \sum_{S' \in S} -\Pr[S']\log_2(\Pr[S'])
$$

For a uniform distribution over the 251 possible values of $S$, the entropy is:

$$
H(U) = \log_2(251) \approx 7.971544
$$

#### 8-bit distribution

From 1.1, the values $0,\ldots,4$ have probability $\frac{2}{256}$ and the remaining 246 values have probability $\frac{1}{256}$.

Therefore:

$$
H(D_8)
=
-5\left(\frac{2}{256}\log_2\left(\frac{2}{256}\right)\right)
-246\left(\frac{1}{256}\log_2\left(\frac{1}{256}\right)\right)
$$

$$
H(D_8) = 7.9609375
$$

#### 64-bit distribution

From 1.2, the values $0,\ldots,68$ have probability

$$
\frac{73\,493\,004\,277\,727\,298}{2^{64}}
$$

and the remaining 182 values have probability

$$
\frac{73\,493\,004\,277\,727\,297}{2^{64}}.
$$

Therefore:

$$
H(D_{64}) =
-69\left(
\frac{73\,493\,004\,277\,727\,298}{2^{64}}
\log_2\left(
\frac{73\,493\,004\,277\,727\,298}{2^{64}}
\right)
\right)
$$

$$
-182\left(
\frac{73\,493\,004\,277\,727\,297}{2^{64}}
\log_2\left(
\frac{73\,493\,004\,277\,727\,297}{2^{64}}
\right)
\right)
$$

which gives approximately:

$$
H(D_{64}) \approx 7.971543553951
$$

Comparing the results:

$$
H(D_8) = 7.9609375
$$

$$
H(D_{64}) \approx 7.971543553951
$$

$$
H(U) \approx 7.971543553951
$$

Therefore, neither distribution is exactly uniform. However, the 64-bit distribution has an entropy extremely close to the maximum entropy of the uniform distribution, while the 8-bit distribution is further from uniform.

### 1.4

Now, we take:

$$
p = 2^7 = 128
$$

As in 1.1, $C$ is an 8-bit string, so there are:

$$
2^8 = 256
$$

possible values of $C$, from $0$ to $255$.

The distribution is defined as:

$$
D(C) = C \bmod 128
$$

For example:

| $C$ | $D(C)$ | $S$ |
|---:|---:|---:|
| 0 | $0 \bmod 128 = 0$ | 0 |
| 1 | $1 \bmod 128 = 1$ | 1 |
| 2 | $2 \bmod 128 = 2$ | 2 |
| $\vdots$ | $\vdots$ | $\vdots$ |
| 127 | $127 \bmod 128 = 127$ | 127 |
| 128 | $128 \bmod 128 = 0$ | 0 |
| 129 | $129 \bmod 128 = 1$ | 1 |
| 130 | $130 \bmod 128 = 2$ | 2 |
| $\vdots$ | $\vdots$ | $\vdots$ |
| 255 | $255 \bmod 128 = 127$ | 127 |

Since:

$$
256 = 128 \times 2
$$

each value $S' \in \{0,\ldots,127\}$ is produced by exactly two different values of $C$.

Therefore:

$$
\Pr[S=S'] = \frac{2}{256} = \frac{1}{128}
$$

for every $S' \in \{0,\ldots,127\}$.

Thus, the distribution is uniform.

The entropy is:

$$
H(D) =
128\left(
-\frac{1}{128}\log_2\left(\frac{1}{128}\right)
\right)
$$

Since:

$$
\log_2\left(\frac{1}{128}\right) = -7
$$

we obtain:

$$
H(D) = 7
$$

Therefore, the distribution has the maximum possible entropy of **7 bits**, confirming that it is uniform.