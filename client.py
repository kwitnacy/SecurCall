import socket
import sys

# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
socket_recv = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

socket_recv.bind(('localhost', 5000))

server_address = ('localhost', 1336)
message = bytes('This is the message.  It will be repeated.', encoding='utf-8')

sent = sock.sendto(message, server_address)

data, server = sock.recvfrom(4096)

print(str(data))