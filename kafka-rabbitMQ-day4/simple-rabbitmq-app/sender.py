import pika

#establish connection with RabbitMQ server
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

#Declare an Exchange
channel.exchange_declare(exchange='user_registration_exchange')

#Declare Queues
channel.queue_declare(queue='registration_success_queue', durable=True)
channel.queue_declare(queue='registration_error_queue', durable=True)
channel.queue_declare(queue='registration_on_hold_queue', durable=True)

#Binding Exchange to queues
channel.queue_bind(exchange='user_registration_exchange',
                       queue='registration_success_queue',
                       routing_key='success')
channel.queue_bind(exchange='user_registration_exchange',
                       queue='registration_error_queue',
                       routing_key='error')

channel.queue_bind(exchange='user_registration_exchange',
                       queue='registration_on_hold_queue',
                       routing_key='on_hold')                                              


#Publish the message to exchange
channel.basic_publish(
    exchange='user_registration_exchange', 
    routing_key='success', body='User Anita Successfully Registered',
    properties=pika.BasicProperties(headers={'email': 'anita@gmail.com'})
    )
channel.basic_publish(
    exchange='user_registration_exchange', 
    routing_key='error', body='User David Failed to Registered',
    properties=pika.BasicProperties(headers={'email': 'david@gmail.com'})
    )
channel.basic_publish(
    exchange='user_registration_exchange', 
    routing_key='on_hold', body='User Tom registration on hold',
    properties=pika.BasicProperties(headers={'email': 'tom@gmail.com'})
    )    

print("All Messages Sent successfully")
connection.close()