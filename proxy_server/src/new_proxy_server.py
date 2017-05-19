#!/usr/bin/python

import os,socket,threading

my_ip = socket.gethostbyname(socket.gethostname())
ftp_control_port = 1995
max_connection = 5 
buffer_size = 1 * 1024


class FTPserver (threading.Thread):
	
	def __init__(self):
		self.control_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.control_socket.bind((my_ip, ftp_control_port))
		threading.Thread.__init__(self)

	def run(self):
		self.control_socket.listen(max_connection)
		while True:
				try:
					conn, addr = self.control_socket.accept()
					client_thread = FTPclientThread(conn, addr)
					client_thread.start()
				except KeyboardInterrupt:
					print("[*] (Proxy)Server Starts To Finishing")
					control_socket.close()
					sys.exit(1)
	
	def stop(self):
		self.control_socket.close()


class FTPclientThread(threading.Thread):
	def __init__(self,conn,addr):
		self.conn = conn
		self.addr = addr
		threading.Thread.__init__(self)

	def run(self):
		print("Start new from {}".format(self.addr))
		self.conn.send('220 Welcome!\r\n'.encode())
		while True:
			cmd = self.conn.recv(buffer_size).decode()
			if not cmd:# when connection close cmd is not other wise has value or has empty value(not null)
				print(cmd)
				break
			else:
				print("Recived: {}".format(cmd))
		print("getOut!")

if __name__ == '__main__':
	ftp = FTPserver()
	ftp.start()