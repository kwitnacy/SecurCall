from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import socket
import pyaudio
import time
import os
import threading
import audioop
import random
import json
import secrets
from pylibsrtp import Policy, Session
from typing import Optional, Union


def my_hash(b: bytes) -> bytes:
    h = hashes.Hash(hashes.SHA256(), default_backend())
    h.update(b)
    return h.finalize()


class Client:
    def __init__(self, server_addr: str = '', server_port: int = 0):
        # --- PYAUDIO CONFIG VARS ---
        self.CHUNK = 512
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = 1
        self.RATE = 44100

        # --- UDP VARS ---
        self.UDP_CONNECTION = None
        self.HOST = '127.0.0.1'
        self.PORT = random.randint(5000, 30000) * 2
        self.TIMESOUT = 10

        # --- RTP/SRTP VARS ---
        self.SEQUENCE_NUM = 0
        self.TIMESTAMP = 0
        self.SSRC = 0
        self.SRTPkey = None
        self.rx_session = None
        self.tx_session = None
        self.call_thread = None
        self.MIC_MUTED = False
        self.AUDIO_MUTED = False

        # --- CLIENT DATA ---
        self.user_data = None

        # --- SIP DATA ---
        self.ONLINE = False
        self.BUSY = False
        self.RUNNING = True
        self.ANSWER = None
        self.GOT_BYE = False
        self.token = None
        self.conversation_token = None
        self.aes_engine = None
        self.caller = {}

        # --- SIP SOCKETS ---
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind((self.HOST, self.PORT + 2))

        self.socket_info = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket_info.bind((self.HOST, self.PORT + 3))

        self.server_addr_main = server_addr
        self.server_port_main = server_port

        self.thread_info = threading.Thread(target=self.info_fun, args=())

    # --- AUTHENTICATION ---
    def sign_in(self, user_name: str = '', passwd: str = '', email: str = '') -> bool:
        mess = bytearray()
        mess.append(0x03)
        mess.append(0x00)
        user_data = {
            'user_name': user_name,
            'passwd_hash': str(my_hash(bytes(passwd, encoding='utf-8')).hex()),
            'email_hash': str(my_hash(bytes(email, encoding='utf-8')).hex()),
            'email': email
        }
        mess.extend(map(ord, str(user_data).replace("'", "\"")))
        res = self.send_req(mess=bytes(mess))
        if res['status'] == 'OK':
            return True
        else:
            return False

    def log_in(self, user_name: str = '', passwd: str = '', email: str = '') -> bool:
        mess = bytearray()
        mess.append(0x01)
        mess.append(0x00)
        user_data = {
            'user_name': user_name,
            'passwd_hash': str(my_hash(bytes(passwd, encoding='utf-8')).hex()),
            'email_hash': str(my_hash(bytes(email, encoding='utf-8')).hex())
        }
        mess.extend(map(ord, str(user_data).replace("'", "\"")))
        res = self.send_req(mess=bytes(mess))

        if res['status'] == 'OK':
            self.ONLINE = True
            self.token = res['token']
            self.user_data = {
                'user_name': user_name,
                'passwd_hash': str(my_hash(bytes(passwd, encoding='utf-8')).hex()),
                'email_hash': self.get_data_from_server()['data']['email_hash'],
            }
            self.thread_info.start()
            return True
        else:
            return False

    def log_out(self) -> dict:
        mess = bytearray()
        mess.append(0x02)
        mess.append(0x00)
        mess.extend(map(ord, str({"token": self.token}).replace("'", "\"")))
        res = self.send_req(mess=bytes(mess))
        self.ONLINE = False
        self.RUNNING = False

        return res

    def close(self) -> None:
        if self.caller:
            self.send_bye(self.caller['user_name'])
        self.RUNNING = False
        res = self.log_out()
        print('quit')
        return res

    # --- SERVER COMMUNICATION ---
    def send_req(self, mess: Union[bytes, bytearray] = None) -> dict:
        server_addr = self.crypto_stuff()
        nonce = os.urandom(12)

        ct = self.aes_engine.encrypt(nonce, bytes(mess), None)

        self.socket.sendto(nonce + ct, server_addr)
        data = self.socket.recv(1024)

        response = self.aes_engine.decrypt(data[:12], data[12:], None)

        j = json.loads(response)

        return j

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
            self.caller = {}
            self.GOT_BYE = True
            to_send_bye = bytearray()
            to_send_bye.append(0x00)
            to_send_bye.append(0x20)
            nounce = os.urandom(12)
            to_send_bye = aes_engine_call.encrypt(nounce, bytes(to_send_bye), None)
            self.socket_info.sendto(nounce + to_send_bye, server_info_addr)
            print('Got BYE sent BYE')
            self.conversation_token = None

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

            self.ANSWER = None
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
            self.caller['user_name'] = j['user_name']
            while True:
                if self.ANSWER is not None:
                    if self.ANSWER:
                        self.send_ok()
                        break
                    elif not self.ANSWER:
                        self.send_nok()
                        break
                time.sleep(1)
            # time.sleep(1)
            # self.send_ok()

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

        j = json.loads(data[2:].decode('utf-8').replace("'", "\""))
        self.caller = {
            'ip_addr': j['ip_addr'],
            'port': j['ip_port'],
            'conversation_token': j['conversation_token'],
            'srtp_security_token': j['srtp_security_token']
        }
        self.conversation_token = j['conversation_token']

        if data[1] == 0x80:
            self.BUSY = True
            self.SRTPkey = bytes.fromhex(self.caller['srtp_security_token'])
            thread_call = threading.Thread(target=self.call, args=[self.caller['ip_addr'], self.caller['port'] - 2])
            thread_call.start()

    def send_nok(self):
        mess = bytearray()
        mess.append(0x00)
        mess.append(0x10)
        nounce = os.urandom(12)
        mess = self.aes_engine_call.encrypt(nounce, bytes(mess), None)
        self.socket_info.sendto(nounce + mess, self.server_info_addr)
        self.caller = {}
        self.conversation_token = None

        print('Send NOK')

    def send_bye(self, user_name: str):
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
        self.caller = {}
        self.conversation_token = None

        return response

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

    # --- SIGNALIZATION ---

    def make_call(self, user_name: str):
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
        elif data[1] == 0x40:
            return json.loads(data.decode('utf-8')[2:].replace("'", "\""))
        else:
            return {"error": "No trying"}

        self.socket.settimeout(15)  # to wait for ringing
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

        self.socket.settimeout(120)  # wainting for OK or for NOK

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
                "client_b_ip_port": j['ip_port']-3,
                "client_b_name": j['user_name'],
                "srtp_security_token": j['srtp_security_token']
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
        return res

    # --- CONTACTS MANAGEMENT ---
    def get_contacts(self) -> dict:
        mess = bytearray()
        mess.append(0x0E)
        mess.append(0x00)
        mess.extend(map(ord, str({
            "token": self.token,
        }).replace("'", "\"")))

        return self.send_req(mess)

    def add_contact(self, user_name: str) -> dict:
        mess = bytearray()
        mess.append(0x04)
        mess.append(0x00)
        mess.extend(map(ord, str({
            "token": self.token,
            "to_add": user_name
        }).replace("'", "\"")))

        return self.send_req(mess)

    def modify_contact(self, user_name: str, data: dict) -> dict:
        mess = bytearray()
        mess.append(0x08)
        mess.append(0x00)
        mess.extend(map(ord, str({
            "token": self.token,
            "to_modify": user_name,
            "contact": data
        }).replace("'", "\"")))

        return self.send_req(mess)

    def delete_contact(self, user_name: str) -> dict:
        mess = bytearray()
        mess.append(0x0C)
        mess.append(0x00)
        mess.extend(map(ord, str({
            "token": self.token,
            "to_delete": user_name
        }).replace("'", "\"")))

        return self.send_req(mess)

    # --- USER DATA ---

    def change_passwd_email_on_server(self, passwd: str = '', email: str = '') -> dict:
        data = {}

        if passwd:
            data['new_passwd_hash'] = str(my_hash(bytes(passwd, encoding='utf-8')).hex())
        if email:
            data['new_email_hash'] = str(my_hash(bytes(email, encoding='utf-8')).hex())
            data['new_email'] = email

        if not data:
            return {
                "status": "OK",
                "mess": "Nothing to change"
            }

        data["token"] = self.token
        data["email_hash"] = self.user_data['email_hash']

        mess = bytearray()
        mess.append(0x0A)
        mess.append(0x00)
        mess.extend(map(ord, str(data).replace("'", "\"")))

        return self.send_req(mess)

    def get_data_from_server(self) -> dict:
        mess = bytearray()
        mess.append(0x20)
        mess.append(0x00)
        mess.extend(map(ord, str({
            "token": self.token,
        }).replace("'", "\"")))

        return self.send_req(mess)

    # --- HISTORY ---
    def get_history(self) -> dict:
        mess = bytearray()
        mess.append(0x06)
        mess.append(0x00)
        mess.extend(map(ord, str({
            "token": self.token,
        }).replace("'", "\"")))

        return self.send_req(mess)

    # --- AUDIO TRANSMISSION ---
    def test(self):
        self.init_UDP_connection()
        self.init_session()
        t_udp_controller = threading.Thread(target=self.udp_controller, args=[self.HOST, self.PORT])
        t_udp_controller.start()
        return True

    def call(self, ip_to_send: str, port_to_send: int):
        self.BUSY = True
        self.init_UDP_connection()
        self.init_session()
        t_udp_controller = threading.Thread(target=self.udp_controller, args=[ip_to_send, port_to_send])
        t_udp_controller.start()
        return True

    def init_session(self):
        self.SEQUENCE_NUM = random.randint(1, 9999)
        self.TIMESTAMP = random.randint(1, 9999)
        self.SSRC = random.randint(1, 9999)
        tx_policy = Policy(key=self.SRTPkey, ssrc_type=Policy.SSRC_ANY_OUTBOUND)
        self.tx_session = Session(policy=tx_policy)
        rx_policy = Policy(key=self.SRTPkey, ssrc_type=Policy.SSRC_ANY_INBOUND)
        self.rx_session = Session(policy=rx_policy)

    def udp_controller(self, ip_to_send, port_to_send):
        inp = self.init_audio_input(ip_to_send, port_to_send)
        output = self.init_audio_output()

        inp.start_stream()
        output.start_stream()
        while self.BUSY: # and inp.is_active() and output.is_active():
            print("ON AIR")
            time.sleep(0.1)
        inp.stop_stream()
        inp.close()
        output.stop_stream()
        output.close()
        self.UDP_CONNECTION.close()
        self.UDP_CONNECTION = None

    def init_audio_input(self, ip_to_send, port_to_send):
        def callback(in_data, frame_count, time_info, status):
            try:
                if self.MIC_MUTED:
                    tmp = 0
                    in_data = audioop.lin2alaw(tmp.to_bytes(1024, 'big'), 2)
                    in_data = b'\x80\x08' + self.SEQUENCE_NUM.to_bytes(2, byteorder='big') + \
                              self.TIMESTAMP.to_bytes(4, byteorder='big') + self.SSRC.to_bytes(4,
                                                                                               byteorder='big') + in_data
                    in_data = self.tx_session.protect(in_data)
                    self.UDP_CONNECTION.sendto(in_data, (ip_to_send, port_to_send))
                else:
                    in_data = audioop.lin2alaw(in_data, 2)
                    in_data = b'\x80\x08' + self.SEQUENCE_NUM.to_bytes(2, byteorder='big') + \
                              self.TIMESTAMP.to_bytes(4, byteorder='big') + self.SSRC.to_bytes(4,
                                                                                               byteorder='big') + in_data
                    in_data = self.tx_session.protect(in_data)
                    self.UDP_CONNECTION.sendto(in_data, (ip_to_send, port_to_send))
            except Exception as e:
                print("UDP sending error:", e)
                return in_data, pyaudio.paComplete

            if self.SEQUENCE_NUM > 65530:
                self.SEQUENCE_NUM = random.randint(1, 9999)
            else:
                self.SEQUENCE_NUM += 1
            self.TIMESTAMP += 1
            return in_data, pyaudio.paContinue

        p = pyaudio.PyAudio()
        stream = p.open(format=self.FORMAT,
                        channels=self.CHANNELS,
                        rate=self.RATE,
                        input=True,
                        frames_per_buffer=self.CHUNK,
                        stream_callback=callback)
        return stream

    def init_audio_output(self):
        def callback(in_data, frame_count, time_info, status):
            while True:
                try:
                    self.UDP_CONNECTION.settimeout(1)
                    in_data, _ = self.UDP_CONNECTION.recvfrom(self.CHUNK * 2)
                    if self.AUDIO_MUTED:
                        in_data = int.to_bytes(0, 1024, 'big')
                    else:
                        in_data = self.rx_session.unprotect(in_data)
                        # print('first: ', len(in_data))
                        in_data = audioop.alaw2lin(in_data[12:], 2)
                        # print('second', len(in_data))
                    self.UDP_CONNECTION.settimeout(None)
                    break
                except socket.timeout as e:
                    # print("Odtwarzanie błąd 1:", e)
                    return in_data, pyaudio.paComplete
            return in_data, pyaudio.paContinue

        p = pyaudio.PyAudio()
        stream = p.open(format=self.FORMAT,
                        channels=self.CHANNELS,
                        rate=self.RATE,
                        output=True,
                        frames_per_buffer=self.CHUNK,
                        stream_callback=callback)
        return stream

    def init_UDP_connection(self):
        self.UDP_CONNECTION = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            self.UDP_CONNECTION.bind((self.HOST, self.PORT))
        except Exception as e:
            pass


if __name__ == "__main__":
    print('GO')

    p = pyaudio.PyAudio()

    info = p.get_host_api_info_by_index(0)
    numdevices = info.get('deviceCount')
    for i in range(0, numdevices):
        if (p.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels')) > 0:
            print("Input Device id ", i, " - ", p.get_device_info_by_host_api_device_index(0, i))

    c = Client()
    c.SRTPkey = secrets.token_bytes(30)
    c.test()
