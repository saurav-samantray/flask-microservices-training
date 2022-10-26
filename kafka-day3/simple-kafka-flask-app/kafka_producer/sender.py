import json 
from kafka import KafkaProducer
from utils.messageutils import generate_message

# Messages will be serialized as JSON 
def serializer(message):
    return json.dumps(message).encode('utf-8')

# Kafka Producer
producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=serializer
)

def send(topic_name, message):
        # Send it to our 'messages' topic
        producer.send(topic_name, message, partition=0)