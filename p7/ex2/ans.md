# Reading the skeleton

The file RSA.py implements textbook RSA on top of the cryptography library: `keygen` produces a
PEM-encoded key pair, `load_pub` and `load_priv` parse the PEM files into integers, eval computes
$m^e mod N$ and `inv` computes $c$.

$d mod N$. Execute python RSA.py and check that the self-test reports
a successful roundtrip. Then read the source code and answer the following:

## Q2.1: Which public exponent is being used? Why that value?

The public exponent being used is $0x10001 = 65537$, set in `keygen`.

It is used because:

- **It is fast.** $65537 = 2^{16} + 1$ has only two 1-bits, so computing
  $m^e \bmod N$ takes just 16 squarings and 1 multiplication.
- **It is prime**, so it is coprime with $\Phi(N)$ and the private exponent
  $d = e^{-1} \bmod \Phi(N)$ exists.
- **It is not too small.** With $e = 3$ and no padding, a small message
  satisfies $m^e < N$, so $c = m^e$ without any reduction and $m$ is just the
  cube root of $c$. For the self-test's $m = 42$, $c$ would be $74088$.

Only $e$ is chosen small. $d$ must stay large and unpredictable, otherwise
the key becomes easy to attack.

## Q2.2: Time `keygen`, `eval` and `inv` for 2048-bit and 4096-bit keys. Which operation dominates? Why is `inv` so much slower than `eval`?

Measured with `timing.py` (mean of 10 `keygen`, 1000 `eval` and 100 `inv`
calls):

| Key size | `keygen` | `eval` | `inv` | `inv` / `eval` |
|---:|---:|---:|---:|---:|
| 2048 bits | 165 ms | 0.11 ms | 16.5 ms | about 150x |
| 4096 bits | 1050 ms | 0.44 ms | 127 ms | about 290x |

**`keygen` dominates.** It has to find two large random primes, which means
testing many random candidates until two of them pass the primality test.
This is also why its time varies between runs.

**`inv` is much slower than `eval` because of the exponent.** Square-and-
multiply does one squaring per bit of the exponent and one multiplication
per 1-bit:

- $e = 65537$ has 17 bits with two 1s: about 17 operations.
- $d$ is about as long as $N$ (2047 bits, with about 1000 ones): about 3000
  operations.

Doubling the key size multiplies `eval` by about 4, because each modular
multiplication works on numbers twice as long. It multiplies `inv` by about
8, because $d$ is also twice as long, so there are twice as many of those
multiplications.

Note that `inv` uses only $n$ and $d$. Using the CRT values already stored in
the private key (`dmp1`, `dmq1`, `iqmp`) would make it about 3–4 times faster.

## Q2.3: What does the code do if the integer encoded by $m$ is not smaller than $N$? Why must it do this?

`eval` refuses it: it raises
`ValueError("Message integer must be less than the modulus n.")`.
`inv` does the same check on the ciphertext $c$.

It must do this because RSA works modulo $N$, so it can only represent
values in $[0, N)$. A message $m \geq N$ would silently be reduced:

$$
c = m^e \bmod N = (m \bmod N)^e \bmod N
$$

so decryption returns $m \bmod N$, not $m$. For example, $m = N + 5$
decrypts to $5$. Different messages ($5$, $N + 5$, $2N + 5$, ...) would give
the same ciphertext, and the original message could not be recovered.
Rejecting $m \geq N$ keeps encryption one-to-one, so decryption is always
correct.

