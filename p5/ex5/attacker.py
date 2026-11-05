
from pathlib import Path
import hashpumpy

OUTPUT = Path("q5_output")

message = (OUTPUT / "message.bin").read_bytes()
digest = (OUTPUT / "digest.txt").read_text().strip()

# The attacker knows or guesses the key length,
# but never reads the key itself.
guessed_key_length = 16

additional_data = b"&admin=true"

forged_digest, forged_message = hashpumpy.hashpump(
    digest,
    message,
    additional_data,
    guessed_key_length
)

if isinstance(forged_message, str):
    forged_message = forged_message.encode("latin-1")

(OUTPUT / "forged_message.bin").write_bytes(forged_message)
(OUTPUT / "forged_digest.txt").write_text(forged_digest)

print("Forged message:", forged_message)
print("Forged SHA-256:", forged_digest)
print("Original and forged messages differ:", message != forged_message)
