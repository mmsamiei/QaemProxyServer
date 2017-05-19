#!/usr/bin/python

import socket, sys
from threading import Thread 

ftp_controll_port = 1998 # my love port
max_connection = 5
buffer_size = 1*1024
host = socket.gethostname() 

class ClientThread (Thread):

	def __init__(self,conn,ip,port):
		Thread.__init__(self)
		self.conn = conn
		self.ip = ip
		self.port = port
		print("[+] New Server Socket Thread Started for {} : {}".format(ip,str(port)))

	def run(self):
		while True:
			data = self.conn.recv(buffer_size).decode()
			print("[+] Server Recived Data: {}".format(data))
			self.conn.send("200 OK".encode())

def start():
	control_conns = []
	control_ips = []
	control_ports = []
	try:	
		control_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		control_socket.bind((host,ftp_controll_port))
		control_socket.listen(max_connection)
		print("[*] Server Started To Listen Port {}".format(ftp_controll_port))
	except Exception :
		print("[*] Unable To Initialize Server Socket")
		sys.exit(2)
	while 1:
		try:
			(conn, (ip,port)) = control_socket.accept()
			control_conns.append(conn)
			control_ips.append(ip)
			control_ports.append(port)
			print(control_conns)
		except KeyboardInterrupt:
			print("[*] Server Starts To Finishing")
			control_conns.close()
			sys.exit(1)
	s.close()

start()


