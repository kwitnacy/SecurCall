from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import socket as s
import threading
import os
import json
import time 

from users import users


class Server():
    def __init__(self) -> None:
        self.HOST = s.gethostbyname(s.gethostname())
        self.HOST = '127.0.0.1'
        self.PORT = 1337
        self.FREE_PORTS = [i for i in range(1338, 1401, 1)]
        self.ONLINE_USERS = {}
        self.CALLS = {}
        self.RUNNING = True
        self.TIMEOUT = 10
 
        self.socket_recv = s.socket(s.AF_INET, s.SOCK_DGRAM)
        self.socket_recv.bind((self.HOST, self.PORT))
        
        self.users = users
        self.thread_main = threading.Thread(target=self.recv_connection, args=())
        self.thread_console = threading.Thread(target=self.console, args=())


    def start(self) -> None:
        self.thread_main.start()
        self.thread_console.start()


    def close_all(self) -> None:
        pass


    def log(self, s: str) -> None:
        with open('log.tip', 'a') as log_file:
            log_file.write(time.strftime('[%h %d %H:%M:%S') + '] ' + s + '\n')


    def log_in(self, j: dict, client_addr: (str, int)) -> dict:
        # find in database and compare password hashes
        if j['user_name'] not in self.users:
            self.log('Trying to log in: ' + str(client_addr[0]) + ':' + str(client_addr[1]) + ', ' + str(j))
            return {
                "status": "Error",
                "mess": "no such user"
            }
        
        if self.users[j['user_name']]['passwd_hash'] == j['passwd_hash']:
            token = os.urandom(32).hex()
            self.log('Login from: ' + str(client_addr[0]) + ':' + str(client_addr[1]) + ', username: ' + j['user_name']
                    + ': success :)')
            self.ONLINE_USERS[token] = self.users[j['user_name']]
            self.ONLINE_USERS[token]['ip_addr'] = client_addr
            self.ONLINE_USERS[token]['busy'] = False
            self.users[j['user_name']]['token'] = token

            return {
                "status": "OK",
                "mess": "Logged in",
                "token": token
            }
        else:
            self.log('Login from: ' + str(client_addr[0]) + ':' + str(client_addr[1]) + ', username: ' + j['user_name']
                    + ': error :( ')
            return {
                "status": "Error",
                "mess": "Wrong password"
            }


    def log_out(self, j, client_a_aes_engine, client_a_addr) -> dict:
        # check if token exists if not log ip 
        try:
            token = j['token']
        except KeyError:
            self.log('Logout from: ' + str(client_addr[0]) + ':' + str(client_addr[1]) + ', username: ' + self.ONLINE_USERS[token]['user_name'] + ': No token :(')
            return {
                "status": "Error",
                "mess": "No token"
            }

        if token in self.ONLINE_USERS:
            self.log('Logout from: ' + str(client_addr[0]) + ':' + str(client_addr[1]) + ', username: ' + self.ONLINE_USERS[token]['user_name'] + ': succes :)')
            del self.ONLINE_USERS[token]
            return {
                "status": "OK",
                "mess": "logged out"
            }
        else:
            self.log('Logout from: ' + str(client_addr[0]) + ':' + str(client_addr[1]) + ', username: ' + self.ONLINE_USERS[token]['user_name'] + ': User not logged in :(')
            return {
                "status": "OK",
                "mess": "User not logged in or doesn't exists"
            }


    def sign_in(self, j: dict, client_addr: (str, int)) -> dict:
        # check if alias is free, save to data base
        try:
            if j['user_name'] in self.users:
                self.log('Sign-in from:' + str(client_addr[0]) + ':' + str(client_addr[1]) + ', username: ' + j['user_name']
                        + ': name taken, account was not created')
                return {
                    "status": "Error",
                    "mess": "Name taken"
                }
            if j['passwd_hash']:
                self.users[j['user_name']] = j
                self.users[j['user_name']]['ip_addr'] = None
                self.users[j['user_name']]['user_ID'] = 0

                self.log('Sign-in from:' + str(client_addr[0]) + ':' + str(client_addr[1]) + ', username: ' +
                        j['user_name'] + ': account was created')
                return {
                    "status": "OK",
                    "mess": "Signed in, account was created"
                }

        except KeyError:
            self.log('Sing-in from' + str(client_addr[0]) + ':' + str(client_addr[1]) + ': wrong json: ' + str(j))
            return {
                "status": "Error",
                "mess": "Wrong json"
            }


    def call(self, j: dict, client_a_addr: (str, int), client_a_aes_engine, server_public_key, server_private_key, s_sock):
        #############################################################################
        # call to somebody :)                                         |             #
        # Get "CALL CLIENT B"                                         |             #
        # Check if client B is online                                 |             #
        #   If is online send to him TRYING                           | !continue!  #
        #   If is ofline send to client A "CLIENT B IS OFFLINE"       | !end!       #
        # Send to client B "CALLING"                                  |             #
        # Send to client A "TRYING" and wait for 15 seconds           |             #
        # Wait for "RINGING" from clien B                             |             #
        #   No respond means network problem                          | !end!       #
        #   "BUSY" means client B is busy                             | !end!       #
        #   "RINGING" means client B is ready for conversation        | !continue!  #
        #                                                             |             #
        # "RINGING" is passed to client A and server sends ACK        |             #
        #to client B. Ringing starts.                                 |             #
        # Client B is obliged to send "OK" or "NOK"                   |             #
        #   "NOK" means client B does not want to talk                | !end!       #
        #   "OK" means client B wants to talk                         | !continue!  #
        # "OK" is passed to client A with client's B IP               |             #
        # Client A sends ACK which is passed to client B              |             #
        # Client A initiates RTP connection.                          |             #
        # Work here is done.                                          |             #
        # Main thread waits for "BYE" and sends it to other client.   |             #
        #############################################################################

        try:
            client_a = self.ONLINE_USERS[j['token']]
        except KeyError:
            self.log("Client A: " + j['user_name'] + " wanted to call but sent no token")
            return {
                "status": "Error",
                "mess": "No token"
            }
        

        to_call = j['to_call']
        try:
            to_call_token = self.users[to_call]['token']
        except KeyError:
            self.log("Client A: " + j['user_name'] + " wanted to call Client B: " + to_call + " but client B does not exist")
            return {
                "status": "Error",
                "mess": "User does not exists"
            }
        if to_call_token not in self.ONLINE_USERS:
            self.log("Client A: " + j['user_name'] + " wanted to call Client B: " + to_call + " but client B is offline")
            return {
                "status": "Error",
                "mess": "User is not online"
            }
        else:
            client_b_ip = self.ONLINE_USERS[to_call_token]['ip_addr']
            client_b_ip = client_b_ip[0], client_b_ip[1] + 1
            client_b_user_name = self.ONLINE_USERS[to_call_token]['user_name']
        
        self.log("client A: " + j['user_name']  + " wants to call client b: " + client_b_user_name)

        # send pub key to client B
        s_sock.sendto(server_public_key, client_b_ip)

        # get pub key from client B
        try:
            client_b_pub_key = s_sock.recv(1024)
        except s.timeout:
            self.log("Client B: " + client_b_user_name + " but client B did not send key")
            return {
                "status": "Error",
                "mess": "Timeout. No key from client b"
            }
        client_b_pub_key = serialization.load_pem_public_key(client_b_pub_key, backend=default_backend())

        # create client_b_aes_engine
        shared_key = server_private_key.exchange(ec.ECDH(), client_b_pub_key)
        derived_key = HKDF(
            algorithm=hashes.SHA256(),
            length=32,
            salt=None,
            info=b'handshake data',
            backend=default_backend()
        ).derive(shared_key)
        client_b_aes_engine = AESGCM(derived_key)

        # send client B "CALL"
        to_send_calling = bytearray()
        to_send_calling.append(0x00)
        to_send_calling.append(0x01)
        to_send_calling.extend(map(ord, str({'user_name': client_a['user_name']})))
        nounce = os.urandom(12)
        to_send_calling = client_b_aes_engine.encrypt(nounce, bytes(to_send_calling), None)
        s_sock.sendto(nounce + to_send_calling, client_b_ip)

        # send client A "TRYING"
        to_send_trying = bytearray()
        to_send_trying.append(0x00)
        to_send_trying.append(0x02)
        nounce = os.urandom(12)
        to_send_trying = client_a_aes_engine.encrypt(nounce, bytes(to_send_trying), None)
        s_sock.sendto(nounce + to_send_trying, client_a_addr)

        # wait 15 seconds for "RINGING" from client B
        #   if no "RINGING" end
        #   else send client A "RINGING"
        s_sock.settimeout(15)
        try:
            data, addr = s_sock.recvfrom(1024)
        except s.timeout:
            self.log("Client B: " + client_b_user_name + " did not send RINGING")
            return {
                "status": "Error",
                "mess": "No Ringing message"
            } 

        if addr != client_b_ip:
            self.log("Client's B IP addres changed")
            return {
                "status": "Error",
                "mess": "Somebody else responsed"
            }
        
        data = client_b_aes_engine.decrypt(data[:12], data[12:], None)
        if data[1] == 0x06:
            self.log("Client B: " + client_b_user_name + " is busy")
            to_send_busy = bytearray()
            to_send_busy.append(0x00)
            to_send_busy.append(0x06)
            nounce = os.urandom(12)
            to_send_busy = client_a_aes_engine.encrypt(nounce, bytes(to_send_busy), None)
            s_sock.sendto(nounce + to_send_busy, client_a_addr)
            return {
                "status": "OK",
                "mess": "Client B is busy"
            }
        elif data[1] != 0x04:
            self.log("Client B: " + client_b_user_name + " sent wrong code")
            return {
                "status": "Error",
                "mess": "Wrong response from client B"
            }
        
        to_send_ringing = bytearray()
        to_send_ringing.append(0x00)
        to_send_ringing.append(0x04)
        nounce = os.urandom(12)
        to_send_ringing = client_a_aes_engine.encrypt(nounce, bytes(to_send_ringing), None)
        s_sock.sendto(nounce + to_send_ringing, client_a_addr)
        
        # get "ACK" from client A
        try:
            data, addr = s_sock.recvfrom(1024)
        except s.timeout:
            # timeout while waiting for ack from client A
            self.log("Client A: " + j['user_name'] + " sent no ACK for RINGING")
            return {
                "status": "Error",
                "mess": "No ACK from client A"
            }

        data = client_a_aes_engine.decrypt(data[:12], data[12:], None)
        if data[1] != 0x80:
            self.log("Client A: " + j['user_name'] + " sent wrong code (instead of ACK): " + str(data[1]))
            return {
                "status": "Error",
                "mess": "Wrong byte from client A instead of ACK"
            }

        to_send_ringing_ACK = bytearray()
        to_send_ringing_ACK.append(0x00)
        to_send_ringing_ACK.append(0x80)
        nounce = os.urandom(12)
        to_send_ringing_ACK = client_b_aes_engine.encrypt(nounce, bytes(to_send_ringing_ACK), None)
        s_sock.sendto(nounce + to_send_ringing_ACK, client_b_ip)

        s_sock.settimeout(120)      # long timeout time because its ringing time
        try:
            data, addr = s_sock.recvfrom(1024)
        except s.timeout:
            self.log('No response (OK/NOK) from Client B: ' + client_b_user_name)
            return {
                "status": "Error",
                "mess": "No response from Client B"
            }

        s_sock.settimeout(self.TIMEOUT)

        data = client_b_aes_engine.decrypt(data[:12], data[12:], None)

        if data[1] == 0x08:
            # OK
            to_send_ok = bytearray()
            to_send_ok.append(0x00)
            to_send_ok.append(0x08)
            to_send_ok.extend(map(ord, str({
                'user_name': client_b_user_name,
                'ip_addr': client_b_ip[0],
                'ip_port': client_b_ip[1]
            }).replace("'", "\"")))
            nounce = os.urandom(12)
            to_send_ok = client_a_aes_engine.encrypt(nounce, bytes(to_send_ok), None)
            s_sock.sendto(nounce + to_send_ok, client_a_addr)
            
        elif data[1] == 0x10:
            # NOK
            to_send_nok = bytearray()
            to_send_nok.append(0x00)
            to_send_nok.append(0x10)
            nounce = os.urandom(12)
            to_send_nok = client_a_aes_engine.encrypt(nounce, bytes(to_send_nok), None)
            s_sock.sendto(nounce + to_send_nok, client_a_addr)
            self.log("Client B: " + client_b_user_name + " rejectced the call")
            return {
                "status": "OK",
                "mess": "Call was rejected"
            }
        else:
            print("Got some shit")
            to_send_nok = bytearray()
            to_send_nok.append(0x00)
            to_send_nok.append(0x10)
            nounce = os.urandom(12)
            to_send_nok = client_a_aes_engine.encrypt(nounce, bytes(to_send_nok), None)
            s_sock.sendto(nounce + to_send_nok, client_a_addr)
            return {
                "status": "Error",
                "mess": "Got some wrong byte"
            }

        try:
            data, addr = s_sock.recvfrom(1024)
        except s.timeout:
            # client A did not send ACK for OK for ringing
            to_send_nack = bytearray()
            to_send_nack.append(0x00)
            to_send_nack.append(0x40)
            nounce = os.urandom(12)
            to_send_nack = client_b_aes_engine.encrypt(nounce, bytes(to_send_nack), None)
            s_sock.sendto(nounce + to_send_nack, client_b_ip)
            return {
                "status": "Error",
                "mess": "Did not receive ACK"
            }

        data = client_a_aes_engine.decrypt(data[:12], data[12:], None)

        if data[1] == 0x80:
            nounce = os.urandom(12)
            to_send_ACK = bytearray()
            to_send_ACK.append(0x00)
            to_send_ACK.append(0x80)
            to_send_ACK = client_b_aes_engine.encrypt(nounce, bytes(to_send_ACK), None)
            s_sock.sendto(nounce + to_send_ACK, client_b_ip)
        else:
            # didnt get ACK
            to_send_nack = bytearray()
            to_send_nack.append(0x00)
            to_send_nack.append(0x40)
            nounce = os.urandom(12)
            to_send_nack = client_b_aes_engine.encrypt(nounce, bytes(to_send_nack), None)
            s_sock.sendto(nounce + to_send_nack, client_b_ip)
            self.log("Client A: " + j['user_name'] + " sent wrong byte: " + str(data[1]))
            return {
                "status": "Error",
                "mess": "Got wrong byte"
            }
        
        self.log("Call was estamblished between Client A: " + j['user_name'] + "and Client B: " + client_b_user_name)
        return {
            "status": "OK",
            "mess": "call was estamblished"
        }


    def bye(self, j: dict, client_a_addr: (str, int), client_a_aes_engine, server_public_key, server_private_key, s_sock):
    # Send BYE frame to users in conversation
    # Get addresses from client a, send to client b BYE
    # Forward ACK from client b to client a
        pass

    def session(self, data, addr, free_port):
        session_socket = s.socket(s.AF_INET, s.SOCK_DGRAM)
        session_socket.bind((self.HOST, free_port))
        session_socket.settimeout(self.TIMEOUT)

        private_key = ec.generate_private_key(ec.SECP384R1, default_backend())
	
        public_key = private_key.public_key()	
	
        public_key_bytes = public_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
	
        session_socket.sendto(public_key_bytes, addr)
	
        client_public_key = serialization.load_pem_public_key(data, backend=default_backend())
	
        shared_key = private_key.exchange(ec.ECDH(), client_public_key)

        derived_key = HKDF(
            algorithm=hashes.SHA256(),
            length=32,
            salt=None,
            info=b'handshake data',
            backend=default_backend()
        ).derive(shared_key)
	
        aesgcm = AESGCM(derived_key)
        
        data, addr = session_socket.recvfrom(1024)
        
        req = aesgcm.decrypt(data[:12], data[12:], None)

        code = req[:2]
        data = json.loads(req[2:].decode('utf-8').replace("'", "\""))

        response = {
            "status": "Error",
            "mess": "wrong byte"
        }

        if code[0] == 0x01:
            response = self.log_in(data, addr)

        elif code[0] == 0x02:
            response = self.log_out(data)

        elif code[0] == 0x03:
            response = self.sign_in(data, addr)

        elif code[0] == 0x04:
            pass
        elif code[0] == 0x05:
            pass
        elif code[0] == 0x06:
            pass
        elif code[1] == 0x01:
            response = self.call(data, addr, aesgcm, public_key_bytes, private_key, session_socket)
        elif code[1] == 0x20:
            response = self.bye(data, addr, aesgcm, public_key_bytes, private_key, session_socket)

        nounce = os.urandom(12)
        ct = aesgcm.encrypt(nounce, json.dumps(response).encode('utf-8'), None)

        session_socket.sendto(nounce + ct, addr)
        
        session_socket.close()
        self.FREE_PORTS.append(free_port)
        self.FREE_PORTS.sort()


    def recv_connection(self):
        print('stated :)')
        self.socket_recv.settimeout(self.TIMEOUT)

        while self.RUNNING:
            try:
                data, addr = self.socket_recv.recvfrom(1024)
                threading.Thread(target=self.session, args=(data, addr, self.FREE_PORTS.pop(), )).start()
            except s.timeout:
                pass

        print('Exited recv thread')


    def console(self):
        commands = ['ousers  	-> prints online users', 
            'users 		-> print all users', 
            'quit/close	-> fucks everything up', 
            'help 		-> help'
            ]
        
        while self.RUNNING:
            command = input('>>>')
            if command == 'ousers':
                print(self.ONLINE_USERS)
            elif command == 'users':
                print(self.users)
            elif command == 'quit' or command == 'close':
                self.close_all()
                self.RUNNING = False
                break
            elif command == 'help':
                for x in commands:
                    print(x)
            else:
                print('wrong command')
                for x in commands:
                    print(x)
        
        print('exited console thread.')


if __name__ == '__main__':
    server = Server()
    server.start()


