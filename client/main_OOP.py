from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from typing import Optional, Union

import atexit
import os
import time
import socket 
import threading
import json


def my_hash(b: bytes) -> bytes:
    h = hashes.Hash(hashes.SHA256(), default_backend())
    h.update(b)
    return h.finalize()


class Client:
    def __init__(self, server_addr: str = '', server_port: int = 0, user_name: str = '', passwd: str = '', email: str =''):
        self.user_data = {
            'user_name' : user_name,
            'passwd_hash' : str(my_hash(bytes(passwd, encoding='utf-8')).hex()),
            'email_hash' : str(my_hash(bytes(email, encoding='utf-8')).hex())
        }

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind((socket.gethostbyname(socket.gethostname()), 4200))

        self.server_addr_main = server_addr
        self.server_port_main = server_port

        self.aes_engine = None

    def crypto_stuff(self) -> (str, int):
        private_key = ec.generate_private_key(ec.SECP384R1, default_backend())
        public_key = private_key.public_key()
        public_key_bytes = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
        
        self.socket.sendto(public_key_bytes, (self.server_addr_main, self.server_port_main))
        data, SERVER_ADDR = self.socket.recvfrom(4096)

        server_public_key = serialization.load_pem_public_key(data, backend=default_backend())
        shared_key = private_key.exchange(ec.ECDH(), server_public_key)
        derived_key = HKDF(
            algorithm=hashes.SHA256(),
            length=32,
            salt=None, 
            info=b'handshake data',
            backend=default_backend()
        ).derive(shared_key)

        self.aes_engine = AESGCM(derived_key)

        return SERVER_ADDR


    def send_req(self, mess: Union[bytes, bytearray] = None) -> dict:
        server_addr = self.crypto_stuff()
        nonce = os.urandom(12)

        ct = self.aes_engine.encrypt(nonce, bytes(mess), None)

        self.socket.sendto(nonce + ct, server_addr)
        data, server_addr = self.socket.recvfrom(1024)

        response = self.aes_engine.decrypt(data[:12], data[12:], None).decode('utf-8')
        
        j = json.loads(response.replace("'", "\""))
        print(j)
"""
        mess = bytearray()
        mess.append(0x20)
        mess.append(0x00)
        nonce = os.urandom(12)

        ct = self.aes_engine.encrypt(nonce, bytes(mess), None)

        self.socket.sendto(nonce + ct, server_addr)

        data = self.socket.recv(1024)

        print(self.aes_engine.decrypt(data[:12], data[12:], None))
"""

c = Client('127.0.0.1', 1337, ';', '123', '13')
#c.crypto_stuff()

user_name = 'test_user'
passwd = 'test_pass'
email = 'test@test.pl'

sign_up_data = {
    'user_name' : user_name,
    'passwd_hash' : str(my_hash(bytes(passwd, encoding='utf-8')).hex()),
    'email_hash' : str(my_hash(bytes(email, encoding='utf-8')).hex())
}

mess = bytearray()
mess.append(0x03)
mess.append(0x00)
mess.extend(map(ord, str(sign_up_data)))

c.send_req(mess=mess)

time.sleep(0.5)

mess = bytearray()
mess.append(0x01)
mess.append(0x00)
mess.extend(map(ord, str(sign_up_data)))

c.send_req(mess=mess)
