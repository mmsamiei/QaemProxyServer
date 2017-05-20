#!/usr/bin/python

import os,socket,threading
import re

my_ip = socket.gethostbyname(socket.gethostname())
ftp_control_port = 1995
max_connection = 5 
buffer_size = 1 * 1024

ceit_host = socket.gethostbyname('ceit.aut.ac.ir')


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
		self.http_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.http_socket.connect((ceit_host,80))


	def run(self):
		print("Start new from {}".format(self.addr))
		self.conn.send('220 Welcome!\r\n'.encode())
		while True:
			cmd = self.conn.recv(buffer_size).decode()
			if not cmd:# when connection close cmd is not other wise has value or has empty value(not null)
				print(cmd)
				break
			else:
				print("Recived Some Command : {} from{} ".format(cmd,self.addr))
				print(cmd.strip()) # .strip() removes all whitespace at the start and end, including spaces, tabs, newlines and carriage returns.
				function = getattr(self,cmd[0:4].strip().upper())
				function(cmd)

	def RMD(self,cmd):
		print("1")
	
	def DELE(self,cmd):
		print("1")		
	
	def RETR(self,cmd):
		print("1")
	
	def LIST(self,cmd):
		print("YES")
		URL_HEAD = "HEAD /~94131090/CN1_Project_Files/ HTTP/1.1\r\nHost: {}\r\n\r\n".format(ceit_host)
		URL_GET = "GET /~94131090/CN1_Project_Files/ HTTP/1.1\r\nHost: {}\r\n\r\n".format(ceit_host)
		self.http_socket.send(URL_GET.encode())
		result = self.http_socket.recv(buffer_size).decode()
		http_status = result[9:12]
		if http_status == "200":
			content_len = self.get_content_len(result)
			self.http_socket.send(URL_GET.encode())
			result = self.http_socket.recv(content_len+1).decode()
			regex = r'<(.*)>'
			matchObj = re.search(regex, result, re.M|re.I)
			print(matchObj.group(0))
			print(matchObj.group(1))
			print(matchObj.group(2))
			
		else :
			print("BAD")	
	
	def QUIT(self,cmd):
		self.conn.send("221 Goodbye.\r\n".encode())
	
	def get_content_len(self, result): # !!!
		a = result.find("Content-Length")+len("Content-Length: ")
		b = a
		while True:
			if(result[b] == '\r'):
				break
			b = b + 1
		i = int(result[a:b])
		return i

if __name__ == '__main__':
	ftp = FTPserver()
	ftp.start()
