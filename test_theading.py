import socket
import threading
import time

def receive_thread(val):
	time.sleep(val)
	print('hej po ', str(val))


def transive_thread(val): 
	time.sleep(val)
	print('hej po ', str(val))



threading.Thread(target=receive_thread, args=(2, )).start()
threading.Thread(target=transive_thread, args=(3, )).start()
threading.Thread(target=transive_thread, args=(4, )).start()
threading.Thread(target=transive_thread, args=(5, )).start()
threading.Thread(target=transive_thread, args=(6, )).start()
threading.Thread(target=transive_thread, args=(7, )).start()

print('hej main 1')
time.sleep(1)
print('hej main 2')


