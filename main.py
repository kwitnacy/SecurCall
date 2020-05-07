import socket
import threading
import time


HOST = '127.0.0.1'
PORT1 = 1336
PORT2 = 1337

socket_recv = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
socket_tran = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

socket_recv.bind((HOST, PORT1))
socket_tran.bind((HOST, PORT2))

to_send = []


def receive_thread(sock):
    while True:
        data, addr = sock.recvfrom(1024)
        print('got: ', data)
        print('from: ', addr)
        to_send.append((addr, 'response:'+str(data)[2:-1]))
    

def transive_thread(sock):
    while True:
        while to_send:
            packet = to_send.pop()
            print('sending: ', packet)
            time.sleep(0.02)
            sock.sendto(bytes(packet[1], encoding='utf-8'), packet[0])


x = threading.Thread(target=receive_thread, args=(socket_recv,))
y = threading.Thread(target=transive_thread, args=(socket_tran,))

x.start()
y.start()
