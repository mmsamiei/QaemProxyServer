import socket 
import time
import threading


#my_ip = socket.gethostbyname(socket.gethostname())
proxy_ip = "192.168.138.146" 
ftp_control_port = 9900
ftp_data_port = ftp_control_port + 1 
buffer_size = 1 * 1024 



controllsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
controllsocket.connect((proxy_ip,ftp_control_port)) 
datasocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
datasocket.connect((proxy_ip, ftp_data_port))
flag = "False"
print(controllsocket.recv(buffer_size).decode())
while True:



	while flag == "False":
		username = input('username:\n')
		password = input('password:\n')
		cmd = "PASV " + username + " "+password
		controllsocket.send(cmd.encode())
		flag = controllsocket.recv(1024).decode()
		print("FALS")
		print(flag)
	cmd = input('\n>>')
	controllsocket.send(cmd.encode())

	if cmd[0:4].upper() == 'QUIT':
                print(controllsocket.recv(2048).decode())
                break;

	elif cmd[0:3].upper() == 'RMD':
		print(controllsocket.recv(2048).decode())


	elif cmd[0:4].upper() == 'DELE':
		print(controllsocket.recv(2048).decode())


	elif cmd[0:4].upper() == 'LIST':
		print(controllsocket.recv(2048).decode())
		print(datasocket.recv(2048).decode())
	
	elif cmd[0:4].upper() == 'RETR':
		response = controllsocket.recv(2048).decode()
		chunks = response.split('*')
		if(chunks[0] == "BeReady"):
			file_name = chunks[1]
			size = (int) (chunks[2])
			#file_name = controllsocket.recv(2048).decode()
			#size = controllsocket.recv(2048).decode()
			data = datasocket.recv(size)
			while len(data) < size: 
                                data = data + datasocket.recv(size)
			with open("../files/"+file_name, 'wb') as f:
				f.write(data)
		else:
			print(response)

	else:
                print(controllsocket.recv(2048).decode())
                print("You Command is Wrong!")


#controllsocket.send("LIST samiei hastam".encode())
#print(datasocket.recv(2048).decode())
#time.sleep(1)
controllsocket.close()
datasocket.close()



