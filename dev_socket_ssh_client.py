import socket, os

client = socket.socket()
client.connect(('localhost', 9999))

while True:
	cmd = input('>>:').strip()
	if len(cmd) == 0: 
		continue
	client.send(cmd.encode('utf-8'))    #  中文转码为ASCII码
	cmd_res_size = client.recv(1024)    #  指定每次接受的数据大小
	received_size = 0
	received_data = b''
	while received_size < int(cmd_res_size.decode()):    # 相等就是收完不用再收
		data = client.recv(1024)
		received_size += len(data)            # 判断每次收到的可能小于1024

		received_data += data
	else:
		print('cmd res recieve done...',received_size)
		print(received_data.decode())

client.close()

