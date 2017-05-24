#!/usr/bin/python

import os,socket,threading
import re
import ipaddress

my_ip = socket.gethostbyname(socket.gethostname())
ftp_control_port = 8400
ftp_data_port = ftp_control_port + 1
max_connection = 5
buffer_size = 1 * 1024

ceit_host = socket.gethostbyname('ceit.aut.ac.ir')


class FTPserver (threading.Thread):
	
	def __init__(self):
		self.control_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.control_socket.bind((my_ip, ftp_control_port))
		self.data_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.data_socket.bind((my_ip, ftp_data_port))
		threading.Thread.__init__(self)


	def run(self):
		self.control_socket.listen(max_connection)
		self.data_socket.listen(max_connection)
		while True:
				try:
					conn, addr = self.control_socket.accept()
					print("1")
					dataconn, addr = self.data_socket.accept()
					print("2")
					client_thread = FTPclientThread(conn, dataconn, addr)
					client_thread.start()
				except KeyboardInterrupt:#TODO kill al threads
					print("[*] (Proxy)Server Starts To Finishing")
					control_socket.close()
					sys.exit(1)
	
	def stop(self):
		self.control_socket.close()


class FTPclientThread(threading.Thread):
	def __init__(self,conn,dataconn,addr):
		self.conn = conn
		self.addr = addr
		self.dataconn = dataconn
		threading.Thread.__init__(self)
		# in the name of god


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
				#try:
				function = getattr(self,cmd[0:4].strip().upper())
				function(cmd)
				#except Exception as e:
				#self.conn.send("We Have Not This Method!".encode())
	def RMD(self, cmd):

		folder = '../cache'
		for the_file in os.listdir(folder):
			file_path = os.path.join(folder, the_file)
			try:
				if os.path.isfile(file_path):
					os.unlink(file_path)
					self.conn.send("All Files Are removed successfully!".encode())
			except Exception as e:
					self.conn.send("An error is happened in process of delete all fills!".encode())
					print(e)


		print("1")
	
	def DELE(self, cmd):
		folder = '../cache'
		file_name = (cmd[4:].strip())
		file_path = os.path.join(folder, file_name)	
		if (os.path.isfile(file_path)):
			os.remove(file_path)
			self.conn.send("File Is Removed Successfully!!".encode())
		else:
			self.conn.send("We haven't Got This File!!".encode())

	
	def RETR(self, cmd):
		print("2222")
		folder = '../cache'
		file_name = (cmd[4:].strip())
		file_path = os.path.join(folder, file_name)
		if( not os.path.isfile(file_path)):
			if(self.download_from_server(file_name)):
				print("I downloaded it!!")
			else:
				self.conn.send("We Have Not This File On File Server!".encode())
				return
		#send to client
		file = open("../cache/" + file_name, 'rb')
		data = file.read()
		self.conn.send(("BeReady*{}*{}".format(file_name, str(len(data)))).encode())
		#self.conn.send(file_name.encode())
		#self.conn.send(str(len(data)).encode())
		self.dataconn.send(data)
	
	def LIST(self,cmd):
		URL_GET = "GET /~94131090/CN1_Project_Files/ HTTP/1.0\r\nHost: {}\r\n\r\n".format(ceit_host)
		self.http_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.http_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self.http_socket.connect((ceit_host,80))
		self.http_socket.send(URL_GET.encode())
		result = self.recvall().decode()
		http_status = result[9:12]
		print(result)
		if http_status == "200":
			regex = re.compile("<a.*>(.*)(\..*)</a>")
			rose = regex.findall(result)
			sended_msg = ""
			for ros in rose:
				sended_msg  = sended_msg + str(ros[0]) + str(ros[1]) + "\r\n"
			print(sended_msg)
			self.conn.send("List Of Files Are Sending!".encode())
			self.dataconn.send(sended_msg.encode())
		else:
			print(result)
			print("BAD REQUEST!")	
	
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

	def recvall(self):
		total_data=bytes()
		while True:
			data = self.http_socket.recv(buffer_size)
			if not data: break
			total_data = total_data + data
			print("!")
		return total_data


	def download_from_server(self, file_name):
		print("SS")
		file_name = file_name.replace(" ","%20")
		URL_HEAD = "HEAD /~94131090/CN1_Project_Files/{} HTTP/1.1\r\nHost: {}\r\n\r\n".format(str(file_name), ceit_host)
		URL_GET = "GET /~94131090/CN1_Project_Files/{} HTTP/1.1\r\nHost: {}\r\n\r\n".format(str(file_name), ceit_host)
		self.http_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.http_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self.http_socket.connect((ceit_host,80))
		self.http_socket.send(URL_GET.encode())
		result = self.recvall()
		http_status = (int)(result[9:12].decode())
		print(http_status)
		if(http_status==200):
			print("RAstA")
			header_border = re.compile(b'\r\n\r\n')
			parts = (header_border.split(result, 1))
			data = parts[1]
			print("HAYHAYHAYHAY")
			file_name = file_name.replace('%20', ' ')
			with open("../cache/" + file_name, 'wb') as f:
			 	f.write(data)
			return True
		else:
			return False


if __name__ == '__main__':
	ftp = FTPserver()
	ftp.start()
