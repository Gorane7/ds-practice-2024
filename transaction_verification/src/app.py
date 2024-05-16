import sys
import os
import re
import datetime
import time
import threading
from collections import defaultdict

from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry import trace

# This set of lines are needed to import the gRPC stubs.
# The path of the stubs is relative to the current file, or absolute inside the container.
# Change these lines only if strictly needed.
FILE = __file__ if '__file__' in globals() else os.getenv("PYTHONFILE", "")
utils_path = os.path.abspath(os.path.join(FILE, '../../../utils/pb/transaction_verification'))
sys.path.insert(0, utils_path)
import transaction_verification_pb2 as transaction_verification
import transaction_verification_pb2_grpc as transaction_verification_grpc

utils_path3 = os.path.abspath(os.path.join(FILE, '../../../utils/pb/suggestions_service'))
sys.path.insert(0, utils_path3)

utils_path = os.path.abspath(os.path.join(FILE, '../../../utils/pb/fraud_detection'))
sys.path.insert(0, utils_path)

import fraud_detection_pb2 as fraud_detection
import fraud_detection_pb2_grpc as fraud_detection_grpc

import suggestions_service_pb2 as suggestions_service
import suggestions_service_pb2_grpc as suggestions_service_grpc

import grpc
from concurrent import futures

resource = Resource(attributes={
    SERVICE_NAME: "transaction_verification"
})

provider = TracerProvider(resource=resource)
processor = BatchSpanProcessor(OTLPSpanExporter(endpoint="http://observability:4318/v1/traces"))
provider.add_span_processor(processor)

trace.set_tracer_provider(provider)
tracer = trace.get_tracer("verification.tracer")

# Create a class to define the server functions, derived from
# transaction_verification_pb2_grpc.HelloServiceServicer
class VerifService(transaction_verification_grpc.VerifServiceServicer):
    def __init__(self):
        self.vector_clock = defaultdict(lambda : [0,0,0])
        self.response = defaultdict(lambda : transaction_verification.VerifyResponse())
        self.die = defaultdict(lambda : False)
        self.part1dep = [0,0,0]
        self.part2dep = [3,5,2]

    def VectorClockUpdate(self, request, context):
        self.vector_clock[request.order_id] = [max(self.vector_clock[request.order_id][i], request.vector_clock[i]) for i in range(len(request.vector_clock))]
        self.vector_clock[request.order_id][0]+=1
        print(f"Clock is {self.vector_clock[request.order_id]}")
        return transaction_verification.Empty_trans()

    # Create an RPC function to say hello
    def Verify(self, request, context):
        with tracer.start_as_current_span("verification") as span:
            self.response[request.order_id].decision = 0
            thread1 = threading.Thread(target=self.verifyPart1, args=(request.order_id, request))
            thread2 = threading.Thread(target=self.verifyPart2, args=(request.order_id, request))
            thread1.start()
            thread2.start()
            thread1.join()
            thread2.join()
            resp = self.response[request.order_id]
            if request.order_id in self.die:
                self.die.pop(request.order_id)
            if request.order_id in self.response:
                self.response.pop(request.order_id)
            if request.order_id in self.vector_clock:
                self.vector_clock.pop(request.order_id)
        return resp
    
    def verifyPart1(self, order_id, request):
        while not self.depCheck(self.vector_clock[order_id],self.part1dep):
            time.sleep(0.1)
            if self.die[order_id]:
                return
        with tracer.start_as_current_span("verification-part1") as span:
            start = time.time()
            decision = 0
            if len(request.items) == 0:
                decision ^= (1<<1)
                print("Transaction failure: empty list of items")
            if request.userInfo.name == "":
                decision ^= (1<<2)
                print("Transaction failure: empty client name")
            if request.userInfo.contact == "":
                decision ^= (1<<3)
                print("Transaction failure: empty client contact info")
            print(f"Bitmap of transaction verification results from part 1: {decision}")
            print(f"Time taken to verify transaction part 1 {round(time.time()-start, 4)}")
            self.response[order_id].decision ^= decision
            self.vector_clock[order_id][0]+=2
            with grpc.insecure_channel('fraud_detection:50051') as channel:
                stub = fraud_detection_grpc.HelloServiceStub(channel)
                vec_clock_msg = fraud_detection.VectorClockInp_fraud()
                vec_clock_msg.vector_clock.extend(self.vector_clock[order_id])
                vec_clock_msg.order_id = order_id
                stub.VectorClockUpdate(vec_clock_msg)

    def verifyPart2(self, order_id, request):
        while self.die[order_id] or not self.depCheck(self.vector_clock[order_id],self.part2dep):
            time.sleep(0.1)
            if self.die[order_id]:
                return
        with tracer.start_as_current_span("verification-part2") as span:
            start = time.time()
            decision = 0
            if request.creditInfo.number == "":
                decision ^= (1<<4)
                print("Transaction failure: empty credit card number")
            if not request.creditInfo.number.isnumeric():
                decision ^= (1<<5)
                print("Transaction failure: non numeric credit card number")
            if not re.match("^(0[0-9]|10|11|12)/[0-9][0-9]$", request.creditInfo.expirationDate):
                decision ^= (1<<6)
                print("Transaction failure: credit card expiration date not legal date")
            month = int(request.creditInfo.expirationDate[:2])
            year = int(request.creditInfo.expirationDate[3:])
            if year < datetime.datetime.now().year%100 or year == datetime.datetime.now().year%100 and month < datetime.datetime.now().month:
                decision ^= (1<<7)
                print("Transaction failure: credit card expired")
            if len(request.creditInfo.cvv) <3:
                decision ^= (1<<8)
                print("Transaction failure: credit card CVV number too short")
            if len(request.creditInfo.cvv) > 4:
                decision ^= (1<<9)
                print("Transaction failure: credit card CVV number too long")
            if not request.creditInfo.cvv.isnumeric():
                decision ^= (1<<10)
                print("Transaction failure: credit card CVV number non numeric")
            print(f"Bitmap of transaction verification results from part 2: {decision}")
            print(f"Time taken to verify transaction part 2 {round(time.time()-start, 4)}")
            self.response[order_id].decision ^= decision
            self.vector_clock[order_id][0]+=2
            with grpc.insecure_channel('suggestions_service:50053') as channel:
                stub = suggestions_service_grpc.SuggestionsServiceStub(channel)
                vec_clock_msg = suggestions_service.VectorClockInp_sugg()
                vec_clock_msg.vector_clock.extend(self.vector_clock[order_id])
                vec_clock_msg.order_id = order_id
                stub.VectorClockUpdate(vec_clock_msg)
    
    def Kill(self, request, context):
        self.die[request.order_id] = True
        time.sleep(1)
        if request.order_id in self.vector_clock:
            self.vector_clock.pop(request.order_id)
        if request.order_id in self.response:
            self.response.pop(request.order_id)
        return transaction_verification.Empty_trans()

    def depCheck(self, vec1, vec2):
        return min([vec1[i]>=vec2[i] for i in range(len(vec1))])

def serve():
    # Create a gRPC server
    server = grpc.server(futures.ThreadPoolExecutor())
    # Add HelloService
    transaction_verification_grpc.add_VerifServiceServicer_to_server(VerifService(), server)
    # Listen on port 50051
    port = "50052"
    server.add_insecure_port("[::]:" + port)
    # Start the server
    server.start()
    print("Server started. Listening on port 50052.")
    # Keep thread alive
    server.wait_for_termination()

if __name__ == '__main__':
    serve()