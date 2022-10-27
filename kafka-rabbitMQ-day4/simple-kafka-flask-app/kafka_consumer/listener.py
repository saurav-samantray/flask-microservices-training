from kafka import KafkaConsumer


def read(ws, topic_name):
    # To consume latest messages and auto-commit offsets
    consumer = KafkaConsumer(topic_name,
                         group_id='demo-group',
                         bootstrap_servers=['localhost:9092'])
    for message in consumer:
        # message value and key are raw bytes -- decode if necessary!
        # e.g., for unicode: `message.value.decode('utf-8')`
        print(f"topic: {message.topic}, partition: {message.partition}, offset: {message.offset}, key: {message.key}, value: {message.value}")
        ws.send({'topic': message.topic, 'partition': message.partition, 'offset': message.offset, 'key': message.key, 'value': message.value})