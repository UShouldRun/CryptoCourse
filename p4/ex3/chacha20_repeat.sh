#!/usr/bin/env bash
set -euo pipefail
IFS=$'\n\t'

# ChaCha20 is a deterministic stream cipher: same key + same nonce =>
# same keystream => same ciphertext for the same plaintext. This script
# demonstrates that with OpenSSL, and that only a fresh nonce changes
# the output.

tmp="$(mktemp -d)"
trap 'rm -rf "$tmp"' EXIT

key="$(openssl rand -hex 32)"     # 256-bit ChaCha20 key
nonce="$(openssl rand -hex 16)"   # 16-byte IV for `enc -chacha20` (4-byte counter + 12-byte nonce, RFC 8439)

printf 'the quick brown fox jumps over the lazy dog\n' > "$tmp/plain.txt"
echo
echo "Plaintext:"
cat "$tmp/plain.txt"
echo

# Encrypt twice with the same key and nonce.
openssl enc -chacha20 -K "$key" -iv "$nonce" -in "$tmp/plain.txt" -out "$tmp/ct1.bin"
openssl enc -chacha20 -K "$key" -iv "$nonce" -in "$tmp/plain.txt" -out "$tmp/ct2.bin"

# Encrypt once more with a fresh nonce.
nonce2="$(openssl rand -hex 16)"
openssl enc -chacha20 -K "$key" -iv "$nonce2" -in "$tmp/plain.txt" -out "$tmp/ct3.bin"

echo "key:   $key"
echo "iv:    $nonce"
echo
echo "ciphertext #1 (same key, same nonce):"
od -A x -t x1z "$tmp/ct1.bin"
echo
echo "ciphertext #2 (same key, same nonce):"
od -A x -t x1z "$tmp/ct2.bin"
echo

if cmp -s "$tmp/ct1.bin" "$tmp/ct2.bin"; then
  echo "identical: reusing the same key and nonce reproduces the ciphertext"
else
  echo "unexpected: ciphertexts differ" >&2
  exit 1
fi

echo
echo "ciphertext #3 (same key, fresh nonce $nonce2):"
od -A x -t x1z "$tmp/ct3.bin"
echo

if cmp -s "$tmp/ct1.bin" "$tmp/ct3.bin"; then
  echo "unexpected: a fresh nonce did not change the ciphertext" >&2
  exit 1
else
  echo "different: a fresh nonce changes the keystream"
fi

# Sanity check: decryption round-trips.
openssl enc -d -chacha20 -K "$key" -iv "$nonce" -in "$tmp/ct1.bin" -out "$tmp/dec.txt"
if ! cmp -s "$tmp/plain.txt" "$tmp/dec.txt"; then
  echo "unexpected: decrypted text does not match plaintext" >&2
  exit 1
fi
echo
echo "Decrypted:"
cat "$tmp/dec.txt"
echo
echo "ok: decrypted text matches the original plaintext"
