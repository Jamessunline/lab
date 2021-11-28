import pika

# auth = pika.PlainCredentials('root', 'root')

connection = pika.BlockingConnection(pika.ConnectionParameters(host='127.0.0.1', port=5672))     #建立socket
	 												
channel = connection.channel()                      # 声明一个传消息的管道

channel.queue_declare(queue='hello')                # 管道里面声明一个queue, 再声明一次是避免producer还没发消息，consumer先运行后报错   

def callback(ch, method, properties, body):
	print('-->',ch,method,properties)
	print("[x] Received %r"% body)

channel.basic_consume(                 
					callback,          # 收到消息，调用callback函数处理消息
					queue='hello',     # 队列的名字  
					no_ack=True)

print('[*] Waiting for messages. To exti press CTRL+C')
channel.start_consuming()
