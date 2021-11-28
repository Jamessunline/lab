import pika


# auth = pika.PlainCredentials('root', 'root')
 
connection = pika.BlockingConnection(pika.ConnectionParameters(host='127.0.0.1',port=5672)) 	 #建立socket

channel = connection.channel()                      # 声明一个传消息的管道

channel.queue_declare(queue='hello')                # 管道里面声明一个名为queue的队列       

channel.basic_publish(exchange='',
					  routing_key='hello',
					  body='Hello world!')

print("[x] Sent 'Hello world!'")
connection.close()
