
def rho(h1):
    print("Hash is " + str(8 * L) + " bits")

    iterations = 0

    while True:
        # Phase 1: Detect a cycle using Floyd's algorithm.
        tortoise = H(h1)
        hare = H(H(h1))
        iterations += 3

        while tortoise != hare:
            tortoise = H(tortoise)
            hare = H(H(hare))
            iterations += 3

        # Phase 2: Find the entry point of the cycle.
        tortoise = h1

        previous_tortoise = None
        previous_hare = None

        while tortoise != hare:
            previous_tortoise = tortoise
            previous_hare = hare

            tortoise = H(tortoise)
            hare = H(hare)
            iterations += 2

        # The predecessors of the cycle entry form a collision,
        # provided that they are different.
        if (
            previous_tortoise is not None
            and previous_hare is not None
            and previous_tortoise != previous_hare
        ):
            return (
                previous_tortoise,
                previous_hare,
                iterations
            )

        # If the walk started inside the cycle, retry.
        h1 = os.urandom(L)
