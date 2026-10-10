**Q2**

The script used was an adaptation of https://github.com/manojpandey/rc4

The plaintext will be 'secret' and the key will be 'abcdefghijklmnop'

Running the script we get the following output:

```
$ python3 rc4.py enc secret

dfa520afd732
```

The same thing can be done with OpenSSL:

```
$ echo -n "secret" | openssl rc4 -provider legacy -provider default -K "6162636465666768696A6B6C6D6E6F70" | xxd -p

dfa520afd732
```

The ```dec.sh``` script can decrypt using OpenSSL or the Python script depending on the argument provided. The key is hardcoded in the scripts, and the ciphertext for 'secret' is provided in this example to be decrypted:

```
# using rc4.py
./dec.sh decpy dfa520afd732 

secret

# using openssl
./dec.sh decopenssl dfa520afd732

secret
```