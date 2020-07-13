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


HOST = '127.0.0.1'
PORT = 1337

FREE_PORTS = [i for i in range(1338, 1501, 1)]

ONLINE_USERS = {}

socket_recv = s.socket(s.AF_INET, s.SOCK_DGRAM)
socket_recv.bind((HOST, PORT))


### Utilities --- begin

def print_data(data, addr):
	print('[' + addr[0] + ':' + str(addr[1]) + '] send -> ' + str(data))

def login():
	pass

def signup():
	pass

def logout():
	pass



def session(data, addr, free_port):
	session_socket = s.socket(s.AF_INET, s.SOCK_DGRAM)
	session_socket.bind((HOST, free_port))
	
	# server private key
	private_key = ec.generate_private_key(ec.SECP384R1, default_backend())
	
	# server public key
	public_key = private_key.public_key()	
	
	# server public key bytes
	public_key_bytes = public_key.public_bytes(
		encoding=serialization.Encoding.PEM,
		format=serialization.PublicFormat.SubjectPublicKeyInfo
	)
	
	# server sends public key bytes to client
	session_socket.sendto(public_key_bytes, addr)
	
	# server gets public key from client (bytes -> obj)
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
	
	while True:
		# request
		data, addr = session_socket.recvfrom(1024)

		mess = aesgcm.decrypt(data[:12], data[12:], None)
		
		nounce = os.urandom(12)
		
		d = str(mess[2:])
		j = json.loads(d[2:-1].replace("'", "\""))
		
		res_code = 0x40

		if mess[0] == 0x01:
			if users[j['user_name']]['passwd_hash'] == j['passwd_hash']:
				print('Login from:', str(addr[0])+':'+str(addr[1]), '-> username: ' + j['user_name'] + ': :) ')
				ONLINE_USERS[j['user_name']] = users[j['user_name']]
				ONLINE_USERS[j['user_name']]['ip_addr'] = addr[0]
				res_code = 0x80
			else:
				print('Login from:', str(addr[0])+':'+str(addr[1]), '-> username: ' + j['user_name'] + ': :( ')
				res_code = 0x40

		elif mess[0] == 0x02:
			users[j['user_name']] = ONLINE_USERS[j['user_name']]
			users[j['user_name']]['ip_addr'] = None
			del(ONLINE_USERS[j['user_name']])

		elif mess[0] == 0x03:
			print('Sign-in from:', str(addr[0])+':'+str(addr[1]), '-> username:', j['user_name'])
			if j['user_name'] in users:
				print('name taken')
				res_code = 0x40
			else:
				print('I will create new user')
				res_code = 0x80

		elif mess[0] == 0x04:
			pass # add user
		elif mess[0] == 0x08:
			pass # Edit contact
		elif mess[0] == 0x0C:
			pass # Delete contact
		
		mess = bytearray(mess)
		mess[0] |= res_code

		ct = aesgcm.encrypt(nounce, bytes(mess), None)

		# response
		session_socket.sendto(nounce + ct, addr)


	
	session_socket.close()
	FREE_PORTS.append(free_port)
	FREE_PORTS.sort()


### Utilities --- end


def recv(socket):
	if socket is None:
		return 1
	
	while True:
		data, addr = socket.recvfrom(1024)
		threading.Thread(target=session, args=(data, addr, FREE_PORTS.pop(), )).start()
	
def check_online_users():
	while True:
		command = input('>>>')
		if command == 'users':
			print(ONLINE_USERS.keys())

threading.Thread(target=recv, args=(socket_recv, )).start()
threading.Thread(target=check_online_users, args=()).start()


