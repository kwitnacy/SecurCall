from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives import serialization

import socket 


HOST = '127.0.0.1'
PORT = 1336

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind((HOST, PORT))


# private key
private_key = ec.generate_private_key(ec.SECP384R1, default_backend())

# public key
public_key = private_key.public_key()

# public key bytes to send
public_key_bytes = public_key.public_bytes(encoding=serialization.Encoding.PEM, format=serialization.PublicFormat.SubjectPublicKeyInfo)


s.sendto(public_key_bytes, (HOST, 1337))

data = s.recv(1024)
# get server's public key 


# perform exchange


# compare shared keys

print(data)
print(public_key_bytes)

