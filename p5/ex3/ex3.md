## Q3 — The Rho Method

### Implementation

The Rho method finds collisions in a hash function using Floyd's cycle-finding algorithm.

It uses two walkers:

- **Tortoise:** advances one hash operation per iteration.
- **Hare:** advances two hash operations per iteration.

When both walkers meet, a cycle has been detected. We can then locate the beginning of the cycle and identify two different inputs that produce the same hash value.

The algorithm requires only a constant amount of memory, unlike a naive birthday attack that stores previously computed hashes.

### Collision verification

A valid collision must satisfy:

1. `x != y`: the two inputs must be different.
2. `H(x) == H(y)`: both inputs must produce the same hash.

The provided script verifies these conditions using an assertion.

### Performance analysis

The hash function is SHA-256 truncated to its first `L` bytes, giving an output length of `8 * L` bits.

For a hash function with `n` output bits, the expected collision-search complexity is approximately:

O(2^(n/2))

Since `n = 8L`, this becomes:

O(2^(4L))

For example:

| L (bytes) | Hash size | Approximate complexity |
|-----------|-----------|------------------------|
| 2         | 16 bits   | 2^8 = 256              |
| 3         | 24 bits   | 2^12 = 4,096           |
| 4         | 32 bits   | 2^16 = 65,536          |
| 5         | 40 bits   | 2^20 = 1,048,576       |

These values represent the expected order of magnitude, not an exact number of iterations.

Increasing `L` by one byte increases the expected computational work by approximately a factor of 16.

The real execution time depends on the number of hash evaluations and the performance of the machine.

### Conclusion

The Rho method can find collisions with approximately O(2^(n/2)) computational complexity while requiring only O(1) additional memory.

For L = 5, the hash output is 40 bits, so the expected collision-search complexity is on the order of 2^20 operations.

This demonstrates how the birthday bound can be exploited without storing a large table of previously computed hash values.