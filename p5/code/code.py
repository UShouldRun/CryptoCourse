from cryptography.hazmat.primitives import hashes
import os, time

L = 5 # output length in bytes (the hash has 8*L bits)

# Something simple to make calling hash functions more succint
def H(X):
	digest = hashes.Hash(hashes.SHA256())
	digest.update(X)
	return (digest.finalize()[0:L])

# Write a function that, starting the walk at h1, finds two values x != y such that H(x) == H(y). Return (x, y, iterations), where iterations counts the steps performed by your walk
def rho(h1):
	print("Hash is "+str(8*L)+" bits")

	# Your code here!!
	x, y, iterations = h1, h1, 0

	return (x, y, iterations)

start = os.urandom(L)
t0 = time.perf_counter()
(x, y, iterations) = rho(start)
elapsed = time.perf_counter() - t0

print("x = " + x.hex() + "  H(x) = " + H(x).hex())
print("y = " + y.hex() + "  H(y) = " + H(y).hex())
print("Iterations: " + str(iterations) + "  Time: %.2fs" % elapsed)
assert (x != y and H(x) == H(y)), "Invalid collision: need x != y (different pre-images) and H(x) == H(y) (the actual collision)"
