import grpc
import persons_pb2
import persons_pb2_grpc

print("Person payload...")

channel = grpc.insecure_channel("localhost:5005")
stub = persons_pb2_grpc.PersonServiceStub(channel)

person = persons_pb2.PersonMessage(
    id=10,
    first_name="Otto",
    last_name="spring",
    company_name='Mc Donald'
)


response = stub.Create(person)
