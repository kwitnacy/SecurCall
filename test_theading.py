import socket
import threading
import time

def receive_thread(val):
	time.sleep(val)
	print('hej po ', str(val))


def transive_thread(val): 
	time.sleep(val)
	print('hej po ', str(val))



x = threading.Thread(target=receive_thread, args=(2, ))
y = threading.Thread(target=transive_thread, args=(3, ))

x.start()
y.start()


print('hej main 1')
time.sleep(1)
print('hej main 2')


