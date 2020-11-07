from .models import Person
from .schemas import (PersonSchema)
from .persons import PersonService
from flask import request, Response, jsonify
from flask_accepts import accepts, responds
from flask_restx import Namespace, Resource
from typing import List
from kafka import KafkaProducer
import json

from flask import Flask

DATE_FORMAT = "%Y-%m-%d"

api = Namespace("UdaConnect", description="Connections via geolocation.")  # noqa
app = Flask(__name__)

@api.route("/persons")
class PersonsResource(Resource):
    @accepts(schema=PersonSchema)
    @responds(schema=PersonSchema)
    def post(self) -> Person:
        payload = request.get_json()
        TOPIC_NAME = 'persons'
        KAFKA_SERVER = 'kafka-app:9092'
        producer = KafkaProducer(bootstrap_servers=KAFKA_SERVER)

        print(payload)
        kafka_data = json.dumps(payload).encode()
        producer.send(TOPIC_NAME, kafka_data)
        producer.flush()

        new_person: Person = PersonService.create(payload)
        return new_person

    @responds(schema=PersonSchema, many=True)
    def get(self) -> List[Person]:
        persons: List[Person] = PersonService.retrieve_all()
        return persons


@api.route("/persons/<person_id>")
@api.param("person_id", "Unique ID for a given Person", _in="query")
class PersonResource(Resource):
    @responds(schema=PersonSchema)
    def get(self, person_id) -> Person:
        person: Person = PersonService.retrieve(person_id)
        return person
