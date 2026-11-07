## A step-by-step prototype of a secure channel

In this excercise, a message was sent in the format:

```
Sequence    IV          Ciphertext      HMAC

8 bytes     16 bytes    Variable        32 bytes
```

First the encryption key must be generated with ```python ./gen.py```

An IV was created to encrypted the message witg AES-CTR.

The receiver checked the HMAC signature and the sequence number to certify integrity.

### PoC

```
# Key generation
$ python ./gen.py  
Keys generated and saved in pw


#Bob script
$ python ./bob.py
Bob read the keys
Bob waiting for Alice...
Bob received (0): Hello Bob
    IV 0e6dc204596c6d472ae6a0ab11fe893b
    CIPHER 45f639e4908cf765ab
    HMAC d4220fca141204ddb21ea8bc15228cf504c04144fc59c8b389fcafe29a9b2c53

Bob sent (0): Hello Alice
    IV af90e774d62b5efda1d6b3469a5dda69
    CIPHER 0aff47a23e6194d46bb745
    HMAC b8b5ea319efec0d8a6a97aa9302ec8b99a5eb8420a70a7fe6305e874e21fb1cd

Bob received (1): I would like to have dinner
    IV d82a09188beca1cca1071f5e0380aef7
    CIPHER f04476e0a136312de7b6048326dff9804b995f8f6b49743aaffd36
    HMAC e64269499e232499c4af2c548949693d17ee3fdf7b0cbce7206846508ecfa874

Bob sent (1): Me too. Same time, same place?
    IV 1bedb24c15eca445002370f9db8b971b
    CIPHER a4192463abadce308054414eaa9de1515cacbcb0c35536fe035d7855e224
    HMAC 9947d68306eaea1070399f5b99ff1ea11ca8edec41e0c4e76ac3381f594741b2

Bob received (2): Sure!
    IV 0dc39e64ed1ac5d4a6f5778547794720
    CIPHER e82f395213
    HMAC 4438b686e34fdb4ddeb85a583cc3618efd56ac310daa183c15aeb32612c1bd3f



#Alice script
$ python ./alice.py
Alice read the keys
Alice sent (0): Hello Bob
    IV  0e6dc204596c6d472ae6a0ab11fe893b
    CIPHER  45f639e4908cf765ab
    HMAC  d4220fca141204ddb21ea8bc15228cf504c04144fc59c8b389fcafe29a9b2c53

Alice received (0): Hello Alice
    IV  af90e774d62b5efda1d6b3469a5dda69
    CIPHER  0aff47a23e6194d46bb745
    HMAC  b8b5ea319efec0d8a6a97aa9302ec8b99a5eb8420a70a7fe6305e874e21fb1cd

Alice sent (1): I would like to have dinner
    IV  d82a09188beca1cca1071f5e0380aef7
    CIPHER  f04476e0a136312de7b6048326dff9804b995f8f6b49743aaffd36
    HMAC  e64269499e232499c4af2c548949693d17ee3fdf7b0cbce7206846508ecfa874

Alice received (1): Me too. Same time, same place?
    IV  1bedb24c15eca445002370f9db8b971b
    CIPHER  a4192463abadce308054414eaa9de1515cacbcb0c35536fe035d7855e224
    HMAC  9947d68306eaea1070399f5b99ff1ea11ca8edec41e0c4e76ac3381f594741b2

Alice sent (2): Sure!
    IV  0dc39e64ed1ac5d4a6f5778547794720
    CIPHER  e82f395213
    HMAC  4438b686e34fdb4ddeb85a583cc3618efd56ac310daa183c15aeb32612c1bd3f
```
