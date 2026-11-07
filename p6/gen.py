import os

with open("pw", "wb") as file:
#              AES-128          HMAC-SHA256
    file.write(os.urandom(16) + os.urandom(32))

print("Keys generated and saved in pw")
