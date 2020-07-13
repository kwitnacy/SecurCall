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


    # TODO
    def log_out(self, j) -> dict:
        # check if token exists if not log ip 
        raise Exception('Not Implemented yet')
        return {}


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



    # TODO
    def call(self, j) -> dict:
        ###############################################################
        # call to somebody :) 
        # Get "CALL CLIENT B"
        # Check if client B is online
        #   If is online send to him TRYING                         !continue!
        #   If is ofline send to client A "CLIENT B IS OFFLINE"     !end!
        # Send to client B "CALLING"
        # Send to client A "TRYING" and wait for 15 seconds
        # Wait for "RINGING" from clien B
        #   No respond means network problem                        !end!
        #   "BUSY" means client B is busy                           !end!
        #   "RINGING" means client B is ready for conversation      !continue!

        # "RINGING" is passed to client A and server sends ACK 
        #to client B. Ringing starts.
        # Client B is obliged to send "OK" or "NOK"
        #   "NOK" means client B does not want to talk              !end!
        #   "OK" means client B wants to talk                       !continue!
        # "OK" is passed to client A with client's B IP
        # Client A sends ACK which is passed to client B
        # Client A initiates RTP connection.
        # Work here is done.
        # Main thread waits for "BYE" and sends it to other client.
        raise Exception('Not Implemented yet')
        return {}

    
    # TODO
    def ringing(self, j) -> dict:
        # signal that client is ringing
        raise Exception('Not Implemented yet')
        return {}


    def session(self, data, addr, free_port):
        session_socket = s.socket(s.AF_INET, s.SOCK_DGRAM)
        session_socket.bind((self.HOST, free_port))

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

        nounce = os.urandom(12)
        ct = aesgcm.encrypt(nounce, json.dumps(response).encode('utf-8'), None)

        session_socket.sendto(nounce + ct, addr)


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


