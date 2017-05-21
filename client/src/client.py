import socket 
import time

host = socket.gethostbyname(socket.gethostname()) 
port = 1997
buffer_size = 1 * 1024 

clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientSocket.connect((host,port)) 
print(clientSocket.recv(buffer_size).decode())
clientSocket.send("LIST samiei hastam".encode())
clientSocket.close()