"""
RSA Primitives: keygen, load_pub, load_priv, eval, inv
Implements the raw RSA mathematical functions (textbook RSA):
  eval: c = m^e mod n
  inv:  m = c^d mod n

keygen produces PEM-encoded keys via the `cryptography` library.
load_pub/load_priv parse a PEM once into the integers eval/inv operate on.
eval/inv inputs and outputs are byte arrays representing big-endian integers.
"""

from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend


# ---------------------------------------------------------------------------
# Key Generation
# ---------------------------------------------------------------------------

def keygen(key_size: int = 2048) -> tuple[bytes, bytes]:
    """
    Generate an RSA key pair.

    Args:
        key_size: RSA modulus size in bits (default 2048).

    Returns:
        (public_key_pem, private_key_pem) as byte arrays (PEM-encoded).
    """
    private_key = rsa.generate_private_key(
        public_exponent=0x10001,  # 65537
        key_size=key_size,
        backend=default_backend(),
    )

    private_key_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),
    )

    public_key_pem = private_key.public_key().public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    )

    return public_key_pem, private_key_pem


# ---------------------------------------------------------------------------
# Key Loading
# ---------------------------------------------------------------------------

def load_pub(public_key_pem: bytes) -> tuple[int, int]:
    """
    Parse a PEM-encoded RSA public key.

    Returns:
        (n, e)
    """
    pub = serialization.load_pem_public_key(public_key_pem, backend=default_backend())
    nums = pub.public_numbers()
    return nums.n, nums.e


def load_priv(private_key_pem: bytes) -> tuple[int, int, int, int, int, int, int]:
    """
    Parse a PEM-encoded RSA private key.

    Returns:
        (n, d, p, q, dmp1, dmq1, iqmp)
    """
    priv = serialization.load_pem_private_key(
        private_key_pem, password=None, backend=default_backend()
    )
    nums = priv.private_numbers()
    return (nums.public_numbers.n, nums.d,
            nums.p, nums.q, nums.dmp1, nums.dmq1, nums.iqmp)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _int_to_bytes(value: int, modulus: int) -> bytes:
    """Encode integer as big-endian bytes, same width as the modulus."""
    length = (modulus.bit_length() + 7) // 8
    return value.to_bytes(length, byteorder="big")


def _bytes_to_int(data: bytes) -> int:
    return int.from_bytes(data, byteorder="big")


# ---------------------------------------------------------------------------
# Eval: c = m^e mod n
# ---------------------------------------------------------------------------

def eval(pk: tuple[int, int], m: bytes) -> bytes:
    """
    Raw RSA eval: c = m^e mod n.

    Args:
        pk: (n, e) as returned by load_pub.
        m:  Message as a big-endian byte array.
            Must represent an integer in [0, n).

    Returns:
        Ciphertext c as a big-endian byte array of width len(n).
    """
    n, e = pk

    m_int = _bytes_to_int(m)
    if m_int >= n:
        raise ValueError("Message integer must be less than the modulus n.")

    c_int = pow(m_int, e, n)
    return _int_to_bytes(c_int, n)


# ---------------------------------------------------------------------------
# Inv: m = c^d mod n
# ---------------------------------------------------------------------------

def inv(sk: tuple[int, ...], c: bytes) -> bytes:
    """
    Raw RSA inv: m = c^d mod n.

    Args:
        sk: (n, d, p, q, dmp1, dmq1, iqmp) as returned by load_priv.
            Only n and d are used here.
        c:  Ciphertext as a big-endian byte array.
            Must represent an integer in [0, n).

    Returns:
        Recovered message m as a big-endian byte array of width len(n).
    """
    n, d = sk[0], sk[1]

    c_int = _bytes_to_int(c)
    if c_int >= n:
        raise ValueError("Ciphertext integer must be less than the modulus n.")

    m_int = pow(c_int, d, n)
    return _int_to_bytes(m_int, n)


# ---------------------------------------------------------------------------
# Quick self-test
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("=== Raw RSA Primitives Demo ===\n")

    # 1. Key generation
    pub_pem, priv_pem = keygen(key_size=2048)
    print("[ keygen ] Generated 2048-bit RSA key pair.")
    print(f"  Public key  : {len(pub_pem)} bytes (PEM)")
    print(f"  Private key : {len(priv_pem)} bytes (PEM)\n")

    # 2. Load keys once
    pk = load_pub(pub_pem)
    sk = load_priv(priv_pem)
    print(f"[ load ] n has {pk[0].bit_length()} bits, e = {pk[1]}\n")

    # 3. Eval:  c = m^e mod n
    # Message must be a valid integer < n; we use a small padded value here.
    m = (42).to_bytes(256, byteorder="big")
    c = eval(pk, m)
    print(f"[ eval ] m (int)     : {int.from_bytes(m, 'big')}")
    print(f"         c (hex[:16]): {c.hex()[:32]}...  ({len(c)} bytes)\n")

    # 4. Inv:  m = c^d mod n
    m_recovered = inv(sk, c)
    print(f"[ inv  ] m recovered : {int.from_bytes(m_recovered, 'big')}")
    print(f"\nRoundtrip OK: {m == m_recovered}")
