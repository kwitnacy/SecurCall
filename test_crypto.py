# from Crypto.PublicKey import RSA

# print(RSA.construct(RSA.generate(2048)))

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.kdf.hkdf import HKDF

server_private_key = ec.generate_private_key(ec.SECP256K1(), default_backend())

host_private_key = ec.generate_private_key(ec.SECP256K1(), default_backend())

shared_key = server_private_key.exchange(ec.ECDH(), host_private_key.public_key())

derived_key = HKDF(
    algorithm=hashes.SHA256(),
    length=64,
    salt=None,
    info=b'handchake',
    backend=default_backend()
).derive(shared_key)

same_shared_key = host_private_key.exchange(ec.ECDH(), server_private_key.public_key())

same_derived_key = HKDF(
    algorithm=hashes.SHA256(),
    length=64,
    salt=None,
    info=b'handchake',
    backend=default_backend()
).derive(same_shared_key)

print(same_derived_key==derived_key)
print(same_derived_key)
print(derived_key)