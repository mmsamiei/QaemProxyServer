import socket 
import time

host = socket.gethostbyname(socket.gethostname()) 
port = 1995
buffer_size = 1 * 1024 

clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientSocket.connect((host,port))
data = clientSocket.recv(buffer_size).decode()
print("recived data is : {}".format(data))
#clientSocket.send("Hello".encode())
time.sleep(1)
clientSocket.send("LIST samiei hastam".encode())
clientSocket.close()