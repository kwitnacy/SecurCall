from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import os

from cryptography.hazmat.primitives.serialization import load_pem_public_key
from cryptography.hazmat.primitives.serialization import Encoding
from cryptography.hazmat.primitives.serialization import PublicFormat

# private_key = ec.generate_private_key(ec.SECP384R1, default_backend())

# # print(dir(private_key.public_key()))
# # print(private_key.public_key().public_numbers().x)

# pub_key = private_key.public_key().public_bytes(encoding=Encoding.PEM, format=PublicFormat.SubjectPublicKeyInfo)
# # print(pub_key.x)
# # print(pub_key.y)
# # print(pub_key.public_key(default_backend()))

# print(pub_key)

# recv_key = load_pem_public_key(pub_key, backend=default_backend())
# print(recv_key.public_numbers().x)
# print(recv_key.public_numbers().y)

##########################################################################################3
import socket

HOST = '127.0.0.1'
PORT = 1337

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind((HOST, PORT))

# private key
private_key = ec.generate_private_key(ec.SECP384R1, default_backend())

# public key
public_key = private_key.public_key()

# public key bytes to send
public_key_bytes = public_key.public_bytes(encoding=serialization.Encoding.PEM, format=serialization.PublicFormat.SubjectPublicKeyInfo)

# get clients's public key 
data = s.recv(1024)

# send public key
s.sendto(public_key_bytes, (HOST, 1336))

# load client's public key
client_public_key = serialization.load_pem_public_key(data, backend=default_backend())

# perform exchange
shared_key = private_key.exchange(ec.ECDH(), client_public_key)

derived_key = HKDF(
    algorithm=hashes.SHA256(),
    length=32,
    salt=None,
    info=b'handshake data',
    backend=default_backend()
).derive(shared_key)

# encrypt/decrypt
mess = b'witaj kliencie!'
aad = b"authenticated but unencrypted data"

aesgcm = AESGCM(derived_key)
nonce = os.urandom(12)

ct = aesgcm.encrypt(nonce, mess, None)

s.sendto(nonce + ct, (HOST, 1336))

data = s.recv(1024)

print(aesgcm.decrypt(data[:12], data[12:], None))
