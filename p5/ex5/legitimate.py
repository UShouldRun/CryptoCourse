
import hashlib
import os
from pathlib import Path

OUTPUT = Path("q5_output")
OUTPUT.mkdir(exist_ok=True)

key = os.urandom(16)
message = b"user=guest&action=view"

digest = hashlib.sha256(key + message).digest()

(OUTPUT / "key.bin").write_bytes(key)
(OUTPUT / "message.bin").write_bytes(message)
(OUTPUT / "digest.txt").write_text(digest.hex())

print("Original message:", message)
print("Original SHA-256:", digest.hex())
print("Files saved in:", OUTPUT)
