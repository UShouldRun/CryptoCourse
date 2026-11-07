import hmac
import os
import socket
import hashlib
import hashlib
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

HOST = "127.0.0.1"
PORT = 5000

send_seq = 0
recv_seq = 0

with open("pw", "rb") as file:
    keys = file.read()
if len(keys) != 48:
    raise ValueError("Invalid pw file: run gen.py first")
encryption_key = keys[:16]
mac_key = keys[16:]
print("Alice read the keys")


def send_message(sock, message):
    global send_seq
    iv = os.urandom(16)
    cipher = Cipher(algorithms.AES(encryption_key), modes.CTR(iv))
    
    ciphertext = cipher.encryptor().update(message.encode())
    sequence_bytes = send_seq.to_bytes(8, "big")
    encrypted_data = sequence_bytes + iv + ciphertext
    tag = hmac.new(mac_key, encrypted_data, hashlib.sha256).digest()
    data = encrypted_data + tag

    sock.sendall(len(data).to_bytes(4, "big") + data)
    print(f"Alice sent ({send_seq}):", message)
    print("    IV ", iv.hex())
    print("    CIPHER ", ciphertext.hex())  
    print("    HMAC ", tag.hex())
    print()
    send_seq += 1



def receive_message(sock):
    global recv_seq
    size = int.from_bytes(receive_exact(sock, 4), "big")
    data = receive_exact(sock, size)

    encrypted_data, received_tag = data[:-32], data[-32:]
    expected_tag = hmac.new(mac_key, encrypted_data, hashlib.sha256).digest()
    if not hmac.compare_digest(expected_tag, received_tag):
        raise ValueError("Message authentication failed")
    sequence = int.from_bytes(encrypted_data[:8], "big")
    if sequence != recv_seq:
        raise ValueError(f"Wrong sequence number: expected {recv_seq}, got {sequence}")


    iv, ciphertext = encrypted_data[8:24], encrypted_data[24:]
    cipher = Cipher(algorithms.AES(encryption_key), modes.CTR(iv))
    message = cipher.decryptor().update(ciphertext).decode()

    print(f"Alice received ({sequence}):", message)
    print(f"    IV ", iv.hex())
    print(f"    CIPHER ", ciphertext.hex())
    print(f"    HMAC ", received_tag.hex())
    print()
    recv_seq += 1


def receive_exact(sock, count):
    result = b""
    while len(result) < count:
        part = sock.recv(count - len(result))
        if not part:
            raise ConnectionError("Connection closed")
        result += part
    return result


with socket.create_connection((HOST, PORT)) as sock:
    send_message(sock, "Hello Bob")
    receive_message(sock)
    send_message(sock, "I would like to have dinner")
    receive_message(sock)
    send_message(sock, "Sure!")
