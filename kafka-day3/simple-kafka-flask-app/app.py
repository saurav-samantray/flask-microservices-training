import time
from datetime import datetime
import random
from flask import Flask, request
from flask_restful import Api, Resource
from kafka_producer import sender
from utils.messageutils import generate_message

app = Flask(__name__)
restful_api = Api(app)

class KafkaApi(Resource):
	def post(self):
		payload = request.json
		topic_name = request.args.get('topic_name')
		if payload == None:
			return {'error': 'No payload provided'}
		if topic_name == None:
			return {'error': 'No topic name provided'}			
		print(f'Producing message @ {datetime.now()} | Message = {str(payload)}')
		sender.send(topic_name, payload)
		return {'success': 'message successfully produced to kafka topic'}


restful_api.add_resource(KafkaApi, '/api/kafka')

if __name__ == '__main__':
	app.run()

# if __name__ == '__main__':
# 	# Infinite loop - runs until you kill the program
# 	while True:
# 		# Generate a message
# 		dummy_message = generate_message()
		
# 		# Send it to our 'messages' topic
# 		print(f'Producing message @ {datetime.now()} | Message = {str(dummy_message)}')
# 		sender.send(dummy_message)
		
# 		# Sleep for a random number of seconds
# 		time_to_sleep = random.randint(1, 11)
# 		time.sleep(time_to_sleep)