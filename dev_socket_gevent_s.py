# -*- coding = utf-8 -*-

from urllib import request
import gevent, time, sys, socket
from gevent import monkey;monkey.patch_all()


                                            # socket server 实现大并发
def server(port):
	s = socket.socket()
	s.bind(('0.0.0.0', port))
	s.listen(500)                            # 500个并发数量排队
	while True:
		cli,addr = s.accept()
		gevent.spawn(handle_request,cli)     #  协程调用下面的方法
		
print('等待传输数据')
def handle_request(conn):
	try:
		while True:
			data = conn.recv(1024)
			print('recv:',data)
			conn.send(data)
			if not data:
				conn.shutdown(socket.SHUT_WR)   # 没有数据关闭

	except Exception as ex:
		print(ex)
	finally:
		conn.close()

if __name__ == '__main__':
	server(8001)