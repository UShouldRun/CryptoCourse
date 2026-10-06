from math import log2

# Shannon entropy: sum of -p * log2(p)
def entropy(probs: [float]) -> float:
    return sum(- p * log2(p) for p in probs)

def entropy_uniform(p: float, n: int) -> float:
    return - n * p * log2(p)

def ex2_1() -> None:
    print("=== Q2.1 ===")
    size_of_s: int = 251 # |S| = p = 251

    # 8 bit strings: |C| = 2 ** 8 = 256
    size_of_c1_1: int = 256

    # Counting 0, 1, ..., |C| - 1 and taking mod 251 cycles through all
    # residues 0..250 again and again. That's |C| // |S| full cycles,
    # so every residue is hit at least that many times.
    # Dividing by |C| turns that count into a probability.
    dist_1_1: [float] = [
        (size_of_c1_1 // size_of_s) / size_of_c1_1 
        for _ in range(size_of_s)
    ]

    # The leftover |C| % |S| values wrap around to residues 0, 1, ...
    # so those get one extra preimage
    for i in range(size_of_c1_1 % size_of_s):
       dist_1_1[i] += 1 / size_of_c1_1


    # 64-bit strings: |C| = 2 ** 64
    size_of_c1_2: int = 2 << (64 - 1)

    # Same idea as before
    dist_1_2 = [
        (size_of_c1_2 // size_of_s) / size_of_c1_2 
        for _ in range(size_of_s)
    ]

    for i in range(size_of_c1_2 % size_of_s):
       dist_1_2[i] += 1 / size_of_c1_2


    # Compare both to log2(251), the entropy of the uniform distribution
    print(f"Entropy(D1_1): { entropy(dist_1_1) }")
    print(f"Entropy(D1_2): { entropy(dist_1_2) }")

def distribution(k: int, p: int) -> [float]:
    n: int = 1 << k  # |C| = 2 ** k
    q: int = n // p  # r values get q + 1 images, the rest q
    r: int = n % p

    # generalization of the process above
    return [
        (q + 1) / n if s < r else q / n 
        for s in range(p)
    ]

def ex2_2() -> None:
    print("=== Q2.2 ===")
    p: int = 251
    print(f"Entropy(D1_1): { entropy(distribution(8, p)) }")
    print(f"Entropy(D1_2): { entropy(distribution(64, p)) }")

    uniform_over_p = entropy_uniform(1 / p, p)
    print(f"entropy of the uniform dist over p = { uniform_over_p }")

    min_k: int   = 8
    diff:  float = abs(uniform_over_p - entropy(distribution(min_k, p)))

    while diff > 1e-6:
        diff = abs(uniform_over_p - entropy(distribution(min_k, p)))
        min_k += 1

    print(f"smallest k = { min_k }")


def main() -> None:
   ex2_1() 
   ex2_2() 

main()
