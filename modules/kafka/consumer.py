from kafka import KafkaConsumer


TOPIC_NAME = 'persons'

consumer = KafkaConsumer(TOPIC_NAME)
for message in consumer:
    print (message)
