from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.kdf.hkdf import HKDF

private_key = ec.generate_private_key(
    ec.SECP384R1(), default_backend()
)

peer_public_key = ec.generate_private_key(
    ec.SECP384R1(), default_backend()
).public_key()

shared_key = private_key.exchange(ec.ECDH(), peer_public_key)

derived_key = HKDF(
    algorithm=hashes.SHA256(),
    length=32,
    salt=None,
    info=b'handshake data',
    backend=default_backend()
).derive(shared_key)

private_key_2 = ec.generate_private_key(
    ec.SECP384R1(), default_backend()
)

peer_public_key_2 = ec.generate_private_key(
    ec.SECP384R1(), default_backend()
).public_key()

shared_key_2 = private_key_2.exchange(ec.ECDH(), peer_public_key_2)

derived_key_2 = HKDF(
    algorithm=hashes.SHA256(),
    length=32,
    salt=None,
    info=b'handshake data',
    backend=default_backend()
).derive(shared_key_2)