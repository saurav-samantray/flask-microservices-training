import pika

#establish connection with RabbitMQ server
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

#Callback methods
def callback(ch, method, properties, body):
	""" 
		body => message body sent by sender/producer
		proeprties => header information
		ch => contains the connection/channel details
		method => contains exhange and queue information
	"""
	print(f"Received Message: {body}")	
	print(f"Triggering success email for : {properties.headers.get('email')}")

def main():
	"""Main method."""
	#Declare an Exchange
	channel.exchange_declare(exchange='user_registration_exchange')

	#Declare Queues
	channel.queue_declare(queue='registration_success_queue', durable=True)

	#Binding Exchange to queues
	channel.queue_bind(exchange='user_registration_exchange',
						queue='registration_success_queue',
						routing_key='success')

	#Consume the message from exchange
	channel.basic_consume("registration_success_queue",
						callback,
						auto_ack=True)  

	try:
		channel.start_consuming()
	except KeyboardInterrupt:
		channel.stop_consuming()                                                              

	connection.close()

if __name__ == '__main__':
	main()