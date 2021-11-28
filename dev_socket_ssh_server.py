import socket, os

server = socket.socket()
server.bind(('localhost',9999))
server.listen()

while True:
	conn,addr = server.accept()
	print('new conn', addr)                 #  显示每次进来的新连接
	while True:
		data = conn.recv(1024)
		if not data:
			print('客户端已断开',data)
			break
		print('执行指令：',data)
		cmd_res= os.popen(data.decode()).read()  # 收到客户端发来的字符串，服务端给客户端发送并执行命令，接受字符串，执行结果也是字符串
		print('before send', len(cmd_res))
		
		if len(cmd_res) == 0:
			cmd_res = 'cmd has no input...'
		
		conn.send(str(len(cmd_res.encode())).encode('utf-8'))               # 先发大小给客户端
		conn.send(cmd_res.encode('utf-8'))    # 命令的结果发送给客户端，IO缓冲区buffer导致分页，
		print('send done')				      # 缓冲区满了系统自动才发上面的为发的内容，新的内容又存入缓冲区
										      # IO缓冲区导致了输出内容分页问题,系统缓冲区是无法修改，
server.close()

