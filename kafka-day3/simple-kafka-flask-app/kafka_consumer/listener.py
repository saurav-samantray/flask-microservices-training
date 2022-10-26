from kafka import KafkaConsumer


def read(topic_name):
    # To consume latest messages and auto-commit offsets
    consumer = KafkaConsumer(topic_name,
                         group_id='demo-group',
                         bootstrap_servers=['localhost:9092'])
    for message in consumer:
        # message value and key are raw bytes -- decode if necessary!
        # e.g., for unicode: `message.value.decode('utf-8')`
        print ("%s:%d:%d: key=%s value=%s" % (message.topic, message.partition,
                                            message.offset, message.key,
                                            message.value))