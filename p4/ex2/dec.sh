#!/bin/bash

operation="$1"
ciphertext="$2"

if [[ "$operation" == "decopenssl" ]]; then
    echo -n "$ciphertext" |
        xxd -r -p |
        openssl rc4 -provider legacy -provider default -K "6162636465666768696A6B6C6D6E6F70"

elif [[ "$operation" == "decpy" ]]; then
    python3 rc4.py dec "$ciphertext" 

else
    echo "Usage: $0 {decopenssl|decpy} <ciphertext>" >&2
    exit 1
fi
