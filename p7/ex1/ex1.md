## Q1 — How hard is factoring?

### Method

`ex1.sage` generates two distinct random primes of $k/2$ bits each with
`random_prime(2^(k/2) - 1, lbound=2^(k/2 - 1))`, keeps the pair only if
$N = p \cdot q$ has exactly $k$ bits, and times `factor(N)`. Each size is run
3 times and the mean is reported.

Run it with:

```
sage ex1.sage
```

For integers, Sage's `factor()` calls PARI's `factorint` (trial division,
then ECM and the Multiple Polynomial Quadratic Sieve, MPQS). The timings below
were measured by calling the same PARI routine (PARI 2.15.4) directly, on a
single core of a 16-thread Linux machine. Running `ex1.sage` gives numbers of
the same magnitude; exact values depend on the machine and on the random
primes.

### Q1.1 — Running times

| $k$ (bits of $N$) | Trial 1 (s) | Trial 2 (s) | Trial 3 (s) | Mean (s) | Ratio to previous |
|---:|---:|---:|---:|---:|---:|
| 128 | 0.020 | 0.015 | 0.017 | 0.017 | — |
| 160 | 0.208 | 0.198 | 0.158 | 0.188 | ×11.1 |
| 192 | 1.042 | 1.074 | 1.592 | 1.236 | ×6.6 |
| 224 | 7.848 | 10.746 | 9.153 | 9.249 | ×7.5 |
| 256 | 83.443 | 87.574 | 72.047 | 81.021 | ×8.8 |

Each extra 32 bits multiplies the time by roughly **8**. Going from 128 to
256 bits (twice the size) multiplies it by about **4800**.

### Q1.2 — Is the growth polynomial?

**No.** For a polynomial $t \approx c \cdot k^e$, the ratio between consecutive
sizes is $((k + 32) / k)^e$, which **shrinks** as $k$ grows. Fitting a
polynomial to these points needs $e \approx 12$, which predicts ratios of
$(160/128)^{12} \approx 14.6$ falling to $(256/224)^{12} \approx 5.0$. The
measured ratios stay at about 7–9, so the polynomial model does not fit.

The data fits a straight line in $\log_2 t$ against $k$:

$$
\log_2 t \text{ grows by } \approx 0.094 \text{ per bit}
\quad\Longrightarrow\quad
\text{the time doubles every} \approx 10.6 \text{ bits.}
$$

That is the behaviour of an exponential-time algorithm over this range. In
theory MPQS is *sub-exponential*:

$$
t \approx c \cdot L_N\!\left[\tfrac12, 1\right]
= c \cdot e^{\sqrt{\ln N \, \ln \ln N}},
$$

which grows faster than any polynomial but slower than $2^{\alpha k}$.
Either way it is **super-polynomial**, which is what the factoring
assumption relies on (week 7, slides 8–9).

### Extrapolation to $k = 2048$

The age of the universe is about $13.8 \times 10^9$ years
$\approx 4.35 \times 10^{17}$ s.

| $k$ | Exponential fit (doubling every 10.6 bits) | Sub-exponential $L[1/2]$ fit |
|---:|---:|---:|
| 512 | $1.4 \times 10^{9}$ s ($\approx 44$ years) | $1.1 \times 10^{9}$ s ($\approx 35$ years) |
| 1024 | $4.2 \times 10^{23}$ s ($\approx 10^{6}$ × universe) | $7.2 \times 10^{18}$ s ($\approx 17$ × universe) |
| 2048 | $3.7 \times 10^{52}$ s ($\approx 10^{35}$ × universe) | $2.0 \times 10^{33}$ s ($\approx 5 \times 10^{15}$ × universe) |

Even with the more optimistic sub-exponential model, factoring a 2048-bit
modulus with this method on one core would take about $10^{15}$ times the
age of the universe. Parallelism changes nothing meaningful: a million cores
still leaves about $10^{9}$ universe lifetimes.

### Caveats

- **The extrapolation is rough.** It stretches five points from 128–256
  bits out to 2048 bits, so only the order of magnitude matters.
- **MPQS is not the best known algorithm.** Large moduli are attacked with
  the General Number Field Sieve, which grows more slowly
  ($\approx \exp(1.9\, n^{1/3} (\log n)^{2/3})$). That is why RSA-768 was
  factored in 2009 and RSA-250 (829 bits) in 2020, even though our MPQS
  extrapolation puts 1024 bits beyond the age of the universe.
- **GNFS still cannot reach 2048 bits.** The slides estimate about $2^{112}$
  operations for a 2048-bit $N$, which is still far out of reach. This is why
  2048-bit RSA is the current minimum and 1024-bit moduli are deprecated.

**Conclusion:** factoring time grows super-polynomially in $k$ (here about
×8 per 32 bits). Doubling the modulus size multiplies the attacker's work
enormously, while honest RSA operations only become slightly slower.
