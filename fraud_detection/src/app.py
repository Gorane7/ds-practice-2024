import sys
import os
import time
import threading
from collections import defaultdict

from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry import metrics
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader

from opentelemetry.exporter.otlp.proto.http.metric_exporter import OTLPMetricExporter

# This set of lines are needed to import the gRPC stubs.
# The path of the stubs is relative to the current file, or absolute inside the container.
# Change these lines only if strictly needed.
FILE = __file__ if '__file__' in globals() else os.getenv("PYTHONFILE", "")
utils_path = os.path.abspath(os.path.join(FILE, '../../../utils/pb/fraud_detection'))
sys.path.insert(0, utils_path)
import fraud_detection_pb2 as fraud_detection
import fraud_detection_pb2_grpc as fraud_detection_grpc

utils_path3 = os.path.abspath(os.path.join(FILE, '../../../utils/pb/suggestions_service'))
sys.path.insert(0, utils_path3)

utils_path2 = os.path.abspath(os.path.join(FILE, '../../../utils/pb/transaction_verification'))
sys.path.insert(0, utils_path2)

import suggestions_service_pb2 as suggestions_service
import suggestions_service_pb2_grpc as suggestions_service_grpc

import transaction_verification_pb2 as transaction_verification
import transaction_verification_pb2_grpc as transaction_verification_grpc

import grpc
from concurrent import futures

resource = Resource(attributes={
    SERVICE_NAME: "fraud_detection"
})

metric_reader = PeriodicExportingMetricReader(OTLPMetricExporter("http://observability:4318/v1/metrics"))
meter_provider = MeterProvider(metric_readers=[metric_reader], resource=resource)
metrics.set_meter_provider(meter_provider)
meter = metrics.get_meter("fraud.detection.meter")
fraud_counter = meter.create_counter("fraud.counter", unit="1", description="Counts the number of fraudulent credit cards detected")

# Create a class to define the server functions, derived from
# fraud_detection_pb2_grpc.HelloServiceServicer
class HelloService(fraud_detection_grpc.HelloServiceServicer):
    def __init__(self):
        self.vector_clock = defaultdict(lambda : [0,0,0])
        self.response = defaultdict(lambda : None)
        self.die = defaultdict(lambda : False)
        self.part1dep = [2,1,0]
        self.part2dep = [2,3,2]

    def VectorClockUpdate(self, request, context):
        self.vector_clock[request.order_id] = [max(self.vector_clock[request.order_id][i], request.vector_clock[i]) for i in range(len(request.vector_clock))]
        self.vector_clock[request.order_id][1] += 1
        print(f"Clock is {self.vector_clock[request.order_id]}")
        return fraud_detection.Empty_fraud()

    # Create an RPC function to say hello
    def SayHello(self, request, context):
        # Create a HelloResponse object
        response = fraud_detection.HelloResponse()
        # Set the greeting field of the response object
        response.greeting = "Hello, " + request.name
        # Print the greeting message
        print(response.greeting)
        # Return the response object
        return response
    
    def DetectFraud(self, request, context):
        thread1 = threading.Thread(target=self.DetectFraudPart1, args=(request.order_id, request))
        thread2 = threading.Thread(target=self.DetectFraudPart2, args=(request.order_id, request))
        thread1.start()
        thread2.start()
        thread1.join()
        thread2.join()

        resp = self.response[request.order_id]
        if request.order_id in self.vector_clock:
            self.vector_clock.pop(request.order_id)
        if request.order_id in self.die:
            self.die.pop(request.order_id)
        if request.order_id in self.response:
            self.response.pop(request.order_id)
        return fraud_detection.FraudResponse() if resp is None else resp
    
    def DetectFraudPart1(self, order_id, request):
        while self.die[order_id] or not self.depCheck(self.vector_clock[order_id],self.part1dep):
            time.sleep(0.1)
            if self.die[order_id]:
                return
        start = time.time()
        response = fraud_detection.FraudResponse()
        response.decision = "thief" in request.name
        if response.decision:
            fraud_counter.add(1)
            print(f"Found fraudulent behaviour")
        print(f"Time taken to detect fraudulent behaviour: {round(time.time()-start, 4)}")
        self.vector_clock[order_id][1]+=1
        print("vector clock: ",self.vector_clock[order_id])
        self.response[order_id] = response
        '''
        with grpc.insecure_channel('fraud_detection:50051') as channel:
            stub = fraud_detection_grpc.HelloServiceStub(channel)
            vec_clock_msg = fraud_detection.VectorClockInp_fraud()
            vec_clock_msg.vector_clock.extend(self.vector_clock[order_id])
            vec_clock_msg.order_id = order_id
            stub.VectorClockUpdate(vec_clock_msg)
        '''

    def DetectFraudPart2(self, order_id, request):
        while self.die[order_id] or not self.depCheck(self.vector_clock[order_id],self.part2dep):
            time.sleep(0.1)
            if self.die[order_id]:
                return
        start = time.time()
        response = fraud_detection.FraudResponse()
        response.decision = "666" in request.creditInfo.number
        if response.decision:
            fraud_counter.add(1)
            print(f"Found fraudulent behaviour")
        print(f"Time taken to detect fraudulent behaviour: {round(time.time()-start, 4)}")
        self.vector_clock[order_id][1]+=2
        self.response [order_id]= response
        with grpc.insecure_channel('transaction_verification:50052') as channel:
            stub = transaction_verification_grpc.VerifServiceStub(channel)
            vec_clock_msg = transaction_verification.VectorClockInp_trans()
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
        return fraud_detection.Empty_fraud()  

    def depCheck(self, vec1, vec2):
        return min([vec1[i]>=vec2[i] for i in range(len(vec1))])


def serve():
    # Create a gRPC server
    server = grpc.server(futures.ThreadPoolExecutor())
    # Add HelloService
    fraud_detection_grpc.add_HelloServiceServicer_to_server(HelloService(), server)
    # Listen on port 50051
    port = "50051"
    server.add_insecure_port("[::]:" + port)
    # Start the server
    server.start()
    print("Server started. Listening on port 50051.")
    # Keep thread alive
    server.wait_for_termination()

if __name__ == '__main__':
    serve()