from datetime import datetime
from flask import Flask, request
from flask_restful import Api, Resource
from flask_sock import Sock
from kafka_producer import sender
from kafka_consumer import listener
from utils.messageutils import generate_message

app = Flask(__name__)
restful_api = Api(app)
sock = Sock(app)

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


@sock.route('/kafka')
def kafka_consumer(ws):
	topic_name = request.args.get('topic_name')
	while True:
		listener.read(ws, topic_name)

if __name__ == '__main__':
	sock.init_app(app)
	app.run(debug=True)