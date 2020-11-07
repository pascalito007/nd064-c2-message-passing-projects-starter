from kafka import KafkaProducer
import json

TOPIC_NAME = 'persons'
KAFKA_SERVER = 'localhost:9092'

producer = KafkaProducer(bootstrap_servers=KAFKA_SERVER)
person = {
    "id": 12,
    "first_name": "Otto",
    "last_name": "helton",
    "company_name": "udacity"
}
producer.send(TOPIC_NAME, json.dumps(person).encode())
producer.flush()
