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

        self.HOST = '127.0.0.1'
        self.PORT = 4200
        self.TIMESOUT = 10

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind((self.HOST, self.PORT))

        self.socket_info = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket_info.bind((self.HOST, self.PORT + 1))

        self.socket_call = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.server_addr_main = server_addr
        self.server_port_main = server_port

        self.aes_engine = None

        self.ONLINE = False
        self.BUSY = False
        self.RUNNING = True

        self.thread_info = threading.Thread(target=self.info_fun, args=())


    def info_fun(self):
        print('info :)')
        
        # listen for datagrams from server about phonecalls
        self.socket_info.settimeout(self.TIMESOUT)
        while self.RUNNING:
            try:
                data, addr = self.socket_info.recvfrom(1024)
                self.get_info(data, addr)
            except socket.timeout:
                pass


    def call_send_pack(self, client_b_info: dict):
        # init connection
        print('Calling somebody')
        print(client_b_info)
        mess = 'hi ' + client_b_info['client_b_name'] + ' how are you doing?'
        mess = mess.encode('utf-8')
        time.sleep(0.5)
        self.socket_call.connect((client_b_info['client_b_ip_addr'], client_b_info['client_b_ip_port'] + 1))
        
        self.socket_call.send(mess)

        data = self.socket_call.recv(1024)

        print(data.decode('utf-8'))

        self.socket_call.close()
        while self.BUSY:
            print('rozmowa')


    def call_get_pack(self):
        # listen for incomming connetcion
        print('Being called')
        self.socket_call.bind((self.HOST, self.PORT + 2))
        self.socket_call.listen(1)
        print('listening')
        conn, addr = self.socket_call.accept()
        print(addr)
        data = conn.recv(1024)
        print(data)
        mess = 'no co tam byczq?'.encode('utf-8')
        conn.send(mess)
        conn.close()
        while self.BUSY:
            print('rozmowa')


    def get_info(self, server_public_bytes: bytes, server_info_addr: (str, int)) -> None:
        print("chyba ktos bedzie dzwonil")
        private_key = ec.generate_private_key(ec.SECP384R1, default_backend())
        public_key = private_key.public_key()
        public_key_bytes = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
        server_public_key = serialization.load_pem_public_key(server_public_bytes, backend=default_backend())
        shared_key = private_key.exchange(ec.ECDH(), server_public_key)

        derived_key = HKDF(
            algorithm=hashes.SHA256(),
            length=32,
            salt=None,
            info=b'handshake data', 
            backend=default_backend()
        ).derive(shared_key)

        aes_engine_call = AESGCM(derived_key)
        
        # Got server public key

        # Sent self public key to server
        self.socket_info.sendto(public_key_bytes, server_info_addr)

        # Got "request"
        data, server_info_addr = self.socket_info.recvfrom(1024)

        data = aes_engine_call.decrypt(data[:12], data[12:], None)

        print(data, "hej hej")
        code = data[:2]
        j = json.loads(data[2:].decode('utf-8').replace("'", "\""))
 
        if code[1] == 0x20:
            self.BUSY = False
            to_send_bye = bytearray()
            to_send_bye.append(0x00)
            to_send_bye.append(0x20)
            nounce = os.urandom(12)
            to_send_bye = aes_engine_call.encrypt(nounce, bytes(to_send_bye), None)
            self.socket_info.sendto(nounce + to_send_bye, server_info_addr)
            print('Got BYE sent BYE')

        elif code[1] == 0x01:
            if self.BUSY:
                to_send_busy = bytearray()
                to_send_busy.append(0x00)
                to_send_busy.append(0x06)
                nounce = os.urandom(12)
                to_send_busy = aes_engine_call.encrypt(nounce, bytes(to_send_busy), None)
                self.socket_info.sendto(nounce + to_send_busy, server_info_addr)
                print('Sent BUSY, PAPA')

                # TODO
                return {}
                
            to_send_ringing = bytearray()
            to_send_ringing.append(0x00)
            to_send_ringing.append(0x04)
            nounce = os.urandom(12)
            to_send_ringing = aes_engine_call.encrypt(nounce, bytes(to_send_ringing), None)
            time.sleep(0.5)
            self.socket_info.sendto(nounce + to_send_ringing, server_info_addr)
            print("sent RINGING")

            # Waitting for ACK for RINGING to start ringing
            data, server_info_addr = self.socket_info.recvfrom(1024)
            data = aes_engine_call.decrypt(data[:12], data[12:], None)

            # Got ACK
            if data[1] != 0x80:
                print('something went wrong, wrong byte (after RINGING)')
                return {
                    "status": "Error",
                    "mess": "got wrong byte after RINGING"
                }

            self.aes_engine_call = aes_engine_call
            self.server_info_addr = server_info_addr
            print('RING RING')
            print(j['user_name'], 'is calling you')
            time.sleep(1)
            self.send_ok()

            """
            # Send OK/NOK
            to_send_ok = bytearray()
            to_send_ok.append(0x00)
            to_send_ok.append(0x08) # OK
            # to_send_ok.append(0x10) # NOK
            nounce = os.urandom(12)
            to_send_ok = aes_engine_call.encrypt(nounce, bytes(to_send_ok), None)
            self.socket_info.sendto(nounce + to_send_ok, server_info_addr)

            print("send OK")
            # print("send NOK")
            
            data, server_info_addr = self.socket_info.recvfrom(1024)
            data = aes_engine_call.decrypt(data[:12], data[12:], None)

            # Get ACK
            if data[1] == 0x80:
                self.BUSY = True
                self.thread_call_get = threading.Thread(target=self.call_get_pack, args=())
                self.thread_call_get.start()
            """

        else:
            print('got shitty mess')
            return None

        # TODO
        return None 
            

    def send_ok(self):
        mess = bytearray()
        mess.append(0x00)
        mess.append(0x08)
        nounce = os.urandom(12)
        mess = self.aes_engine_call.encrypt(nounce, bytes(mess), None)
        self.socket_info.sendto(nounce + mess, self.server_info_addr)

        print('Send OK')

        data, server_info_addr = self.socket_info.recvfrom(1024)
        data = self.aes_engine_call.decrypt(data[:12], data[12:], None)

        if data[1] == 0x80:
            self.BUSY = True
            self.thread_call_get = threading.Thread(target=self.call_get_pack, args=())
            self.thread_call_get.start()


    def send_nok(self):
        mess = bytearray()
        mess.append(0x00)
        mess.append(0x10)
        nounce = os.urandom(12)
        mess = self.aes_engine_call.encrypt(nounce, bytes(mess), None)
        self.socket_info.sendto(nounce + mess, self.server_info_addr)

        print('Send NOK')


    def crypto_stuff(self) -> (str, int):
        private_key = ec.generate_private_key(ec.SECP384R1, default_backend())
        public_key = private_key.public_key()
        public_key_bytes = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
        
        self.socket.sendto(public_key_bytes, (self.server_addr_main, self.server_port_main))
        data, SERVER_ADDR = self.socket.recvfrom(1024)

        print(data)

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
        data = self.socket.recv(1024)

        response = self.aes_engine.decrypt(data[:12], data[12:], None)

        j = json.loads(response)

        return j


    def sign_in(self) -> bytes:
        mess = bytearray()
        mess.append(0x03)
        mess.append(0x00)
        mess.extend(map(ord, str(self.user_data).replace("'", "\"")))
        res = self.send_req(mess=bytes(mess))
    

    def log_in(self) -> None:
        mess = bytearray()
        mess.append(0x01)
        mess.append(0x00)
        mess.extend(map(ord, str(self.user_data).replace("'", "\"")))
        res = self.send_req(mess=bytes(mess))

        if res['status'] == 'OK':
            self.ONLINE = True
            self.token = res['token']
            self.thread_info.start()


    def make_call(self, user_name: str) -> bytes:
        mess = bytearray()
        mess.append(0x00)
        mess.append(0x01)
        mess.extend(map(ord, str({
            "to_call": user_name,
            "token": self.token,
            "user_name": self.user_data['user_name']
            }).replace("'", "\"")))

        server_addr = self.crypto_stuff()
        nounce = os.urandom(12)
        ct = self.aes_engine.encrypt(nounce, bytes(mess), None)

        # sending CALLING to server
        self.socket.sendto(nounce + ct, server_addr)
        
        # waiting for TRYING
        data, addr = self.socket.recvfrom(1024)
        data = self.aes_engine.decrypt(data[:12], data[12:], None)
        print(data.decode('utf-8'))

        if data[1] == 0x02:
            print("TRYING")
        else:
            return {"error": "No trying"}

        self.socket.settimeout(15) # to wait for ringing
        try:
            data, addr = self.socket.recvfrom(1024)
        except socket.timeout:
            return {
                "status": "Error",
                "mess": "Got no RINGING"
            }

        data = self.aes_engine.decrypt(data[:12], data[12:], None)

        if data[1] == 0x04:
            print(user_name + '\'s phone is ringing')
        elif data[1] == 0x06:
            print(user_name + ' is busy')
            return {
                "status": "Error",
                "mess": "Client is busy"
            }
        else:
            return {
                "status": "Error",
                "mess": "Got wrong byte"
            }

        mess = bytearray()
        mess.append(0x00)
        mess.append(0x80)
        nounce = os.urandom(12)
        mess = self.aes_engine.encrypt(nounce, bytes(mess), None)
        self.socket.sendto(nounce + mess, addr)

        self.socket.settimeout(120) # wainting for OK or for NOK

        try:
            data, addr = self.socket.recvfrom(1024)
        except socket.timeout:
            return {
                "status": "Error",
                "mess": "No reaction (OK/NOK)"
            }

        data = self.aes_engine.decrypt(data[:12], data[12:], None)
        print(data)
        
        res = {}
        client_b_info = {}
        flag_ok = False

        if data[1] == 0x08:
            # OK
            j = json.loads(data[2:].decode('utf-8').replace("'", "\""))
            res = {
                "status": "OK",
                "mess": "call is estanblished",
                "client_b_ip_addr": j['ip_addr'],
                "client_b_ip_port": j['ip_port'],
                "client_b_name": j['user_name']
            }
            client_b_info = {
                "client_b_ip_addr": j['ip_addr'],
                "client_b_ip_port": j['ip_port'],
                "client_b_name": j['user_name']
            }
            self.conversation_token = j['conversation_token']
            flag_ok = True
            print("call starts")
        elif data[1] == 0x10:
            # NOK
            res = {
                "status": "Error",
                "mess": "Call was rejected"
            }
            print("call rejected")
        else:
            return {
                "status": "Error",
                "mess": "Wrong frame (waited for NOK or OK)"
            }

        mess = bytearray()
        mess.append(0x00)
        mess.append(0x80)
        nounce = os.urandom(12)
        mess = self.aes_engine.encrypt(nounce, bytes(mess), None)
        self.socket.sendto(nounce + mess, addr)

        if flag_ok:
            self.thread_call_init = threading.Thread(target=self.call_send_pack, args=(client_b_info, ))
            self.thread_call_init.start()

        return res


    def send_bye(self, user_name: str) -> bytes:
        mess = bytearray()
        mess.append(0x00)
        mess.append(0x20)
        mess.extend(map(ord, str({
            "called": user_name,
            "token": self.token,
            "user_name": self.user_data['user_name'],
            "conversation_token": self.conversation_token
            }).replace("'", "\"")))

        server_addr = self.crypto_stuff()
        nounce = os.urandom(12)
        ct = self.aes_engine.encrypt(nounce, bytes(mess), None)

        self.socket.sendto(nounce + ct, server_addr)

        data, addr = self.socket.recvfrom(1024)

        response = self.aes_engine.decrypt(data[:12], data[12:], None)
        
        print(response)

        self.BUSY = False
        self.conversation_token = None

        return response



c = Client(
    server_addr='127.0.0.1',
    server_port=1337,
    user_name='client_b', 
    passwd = 'test_pass_client_b',
    email='test_email_b'
)

c.sign_in()
c.log_in()

