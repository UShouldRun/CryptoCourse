
import hashlib
from pathlib import Path

output = Path("q5_output")

key = (output / "key.bin").read_bytes()
original = (output / "message.bin").read_bytes()
forged = (output / "forged_message.bin").read_bytes()
forged_digest = (output / "forged_digest.txt").read_text().strip()

actual_digest = hashlib.sha256(key + forged).hexdigest()

assert original != forged
assert actual_digest == forged_digest

print("Length extension attack successful!")