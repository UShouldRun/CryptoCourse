import random
import string


# Gens key
def gen():
    letters = list(string.ascii_lowercase)
    random.shuffle(letters)
    return ''.join(letters)


# Encrypts from file to file
def encrypt(plain, cipher, key):
    table = str.maketrans(string.ascii_lowercase, key)
    with open(plain) as f_in, open(cipher, 'w') as f_out:
        f_out.write(f_in.read().translate(table))


# Decrypts form file to file
def decrypt(cipher, plain, key):
    table = str.maketrans(key, string.ascii_lowercase)
    with open(cipher) as f_in, open(plain, 'w') as f_out:
        f_out.write(f_in.read().translate(table))

# k = gen()
# encrypt("plaintext.txt", "ciphertext.txt", k)
# decrypt("ciphertext.txt", "decryption.txt", k)

english_1gram = [
    "e",
    "t",
    "a",
    "o",
    "n",
    "i",
    "h",
    "s",
    "r",
    "l",
    "d",
    "u",
    "c",
    "m",
    "w",
    "y",
    "f",
    "g",
    "p",
    "b",
    "v",
    "k",
    "j",
    "x",
    "q",
    "z"
]

english_2gram = [
    "th", "he", "in", "en", "nt", "re", "er", 
    "an", "ti", "es", "on", "at", "se", "nd", 
    "or", "ar", "al", "te", "co", "de", "to",
    "ra", "et", "ed", "it", "sa", "em", "ro" 
]

english_3gram = [
    "the", "and", "tha", "ent", "ing", "ion", 
    "tio", "for", "nde", "has", "nce", "edt", 
    "tis", "oft", "sth", "men" 
]

c_1gram = [
    "i",                                                             
    "n",                                                             
    "a",                                                             
    "e",                                                             
    "p",                                                             
    "u",                                                             
    "q",                                                             
    "c",
    "s",
    "m",                                                             
    "r",                                                             
    "t",                                                             
    "o",                                                             
    "d",                                                             
    "f",                                                             
    "b",                                                             
    "z",
    "x",
    "h",                                                              
    "y"
]

c_2gram = [
    "us",
    "ac",
    "ea",
    "ai",
    "ip",
    "re",                                                           
    "no",
    "pa",
    "nn",
    "im",
    "nq",
    "na",
    "bn",
    "ri",
    "fn",
    "pu"
]

c_3gram = [
    "pac",
    "usi",
    "bnd",
    "nai",
    "ndt",
    "nri",
    "ire",
    "rea",
    "eac",
    "aci",
    "qno",
    "spu",
    "ann",
    "nna",
    "aix",
    "ixa",
    "xan",
    "ano",
    "nom",
    "ace",
]


with open("ciphertext.txt") as f_in:
    ciphertext = f_in.read()

    table1 = str.maketrans(
        ''.join(english_1gram[:len(c_1gram)]), 
        ''.join(c_1gram)
    )
    mapped_1gram = ciphertext.translate(table1)

    map_2gram = {
        c_2gram[i]: english_2gram[i]
        for i in range(min(len(c_2gram), len(english_2gram)))
    }
    
    chunks_2gram = [
        ciphertext[i : i + 2] 
        for i in range(0, len(ciphertext), 2)
    ]
    for i in range(len(chunks_2gram)):
        if chunks_2gram[i] in map_2gram:
            chunks_2gram[i] = map_2gram[chunks_2gram[i]]
    mapped_2gram = ''.join(chunks_2gram)

    map_3gram = {
        c_3gram[i]: english_3gram[i]
        for i in range(min(len(c_3gram), len(english_3gram)))
    }
    
    chunks_3gram = [
        ciphertext[i : i + 3] 
        for i in range(0, len(ciphertext), 3)
    ]
    for i in range(len(chunks_3gram)):
        if chunks_3gram[i] in map_3gram:
            chunks_3gram[i] = map_3gram[chunks_3gram[i]]
    mapped_3gram = ''.join(chunks_3gram)

    matches123 = [
        (ciphertext[i], mapped_1gram[i])
        for i in range(len(ciphertext))
        if mapped_1gram[i] == mapped_2gram[i] == mapped_3gram[i]
    ]

    matches12 = [
        (ciphertext[i], mapped_1gram[i])
        for i in range(len(ciphertext))
        if mapped_1gram[i] == mapped_2gram[i]
    ]

    matches13 = [
        (ciphertext[i], mapped_1gram[i])
        for i in range(len(ciphertext))
        if mapped_1gram[i] == mapped_3gram[i]
    ]

    matches23 = [
        (ciphertext[i], mapped_2gram[i])
        for i in range(len(ciphertext))
        if mapped_2gram[i] == mapped_3gram[i]
    ]

    print(set(matches123 + matches12 + matches13 + matches23))
