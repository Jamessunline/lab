# -*- coding = utf-8 -*-    

from urllib import request
import gevent, time, sys, socket
from gevent import monkey;monkey.patch_all()


# HOST = 'localhost'
# PORT = '8001'

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('localhost',8001))                                      # 以元组形式发送IP，port

while True:
	msg = bytes(input('>>:'),encoding='utf-8')
	s.sendall(msg)
	if len(msg) == 0:                      # 发送空消息不会卡死
		continue
	data = s.recv(1024)

	# print('Received', data)                  #  发给server端后，server端再发回给客户端

s.close()


