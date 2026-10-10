**Q1.1**

- $` 1 + x + x^3 `$ :

```
101
010
101

Loop of size 2
```

- $` 1 + x + x^4 `$ :

```
0101
1011
0110
1100
1001
0010
0100
1000
0001
0011
0111
1111
1110
1101
1010
0101

Loop of size 15
```


- $` 1 + x^2 + x^3 + x^4 `$ :


```
1100
1000
0001
0010
0101
1011
0110
1100

Loop of size 7
```

We can conclude $` 1 + x + x^4 `$ is primitive, since the size of the loop is equal to $`2^n - 1`$ where *n* is the degree of the polynomial.


**Q1.2**

The best polynomial would be the primitive one, since it maximizes the period and loops over a larger sample, making it more secure (still insecure by itself).


**Q1.3**

```
F = GF(2)
R.<x> = PolynomialRing(F)
f = 1 + x + x^3
print(f.is_irreducible())
f = 1 + x + x^4
print(f.is_irreducible())
f = 1 + x^2 + x^3 + x^4
print(f.is_irreducible())

True
True
False
```

$` 1 + x + x^3 `$ and $` 1 + x + x^4 `$ are irreducible.