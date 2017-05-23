import socket 
import time
import threading


host = socket.gethostbyname(socket.gethostname()) 
port = 2011
buffer_size = 1 * 1024 

class Client(threading.Thread):

	def __init__(self):
		self.clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.clientSocket.connect((host,port)) 
		print(clientSocket.recv(buffer_size).decode())
		threading.Thread.__init__(self)



controllsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
controllsocket.connect((host,port)) 
print(controllsocket.recv(buffer_size).decode())

datasocket = 


controllsocket.send("LIST samiei hastam".encode())



time.sleep(1)
clientSocket.close()