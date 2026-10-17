The hashes that are not collision resistant are:

**3**, because the hash value is static, so H(m0) = H(m1) = H(64)

**5**, because there are only 1024 possible hash values, so if we try to hash 1025 messages, there will be for sure some collision.

**6**, because messages where the last 2 bits differ will produce the same hash. 

For example: 

m0 = 000, 

m0 = 011. 

H(m0) = H(m1) = H(0)