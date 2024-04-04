import sys
import os
import time
import threading

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

import suggestions_service_pb2 as suggestions_service
import suggestions_service_pb2_grpc as suggestions_service_grpc

import grpc
from concurrent import futures

# Create a class to define the server functions, derived from
# fraud_detection_pb2_grpc.HelloServiceServicer
class HelloService(fraud_detection_grpc.HelloServiceServicer):
    def __init__(self):
        self.vector_clock = [0,0,0,0,0]
        self.request = None
        self.response = None
        self.part1dep = [1,0,0,0,0]
        self.part2dep = [0,1,0,0,0]

    def VectorClockUpdate(self, request, context):
        self.vector_clock = [max(self.vector_clock[i], request.vector_clock[i]) for i in range(len(self.vector_clock))]
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
        self.request = request
        thread1 = threading.Thread(target=self.DetectFraudPart1)
        thread2 = threading.Thread(target=self.DetectFraudPart2)
        thread1.start()
        thread2.start()
        thread1.join()
        thread2.join()
        return self.response
    
    def DetectFraudPart1(self):
        while not self.depCheck(self.vector_clock,self.part1dep):
            time.sleep(0.1)
        request = self.request
        start = time.time()
        response = fraud_detection.FraudResponse()
        response.decision = "thief" in request.name
        if response.decision:
            print(f"Found fraudulent behaviour")
        print(f"Time taken to detect fraudulent behaviour: {round(time.time()-start, 4)}")
        self.vector_clock[2]+=1
        self.response = response
        with grpc.insecure_channel('suggestions_service:50053') as channel:
            stub = suggestions_service_grpc.SuggestionsServiceStub(channel)
            vec_clock_msg = suggestions_service.VectorClockInp_sugg()
            vec_clock_msg.vector_clock.extend(self.vector_clock)
            stub.VectorClockUpdate(vec_clock_msg)
        
    def DetectFraudPart2(self):
        while not self.depCheck(self.vector_clock,self.part2dep):
            time.sleep(0.1)
        request = self.request
        start = time.time()
        response = fraud_detection.FraudResponse()
        response.decision = "thief" in request.name
        if response.decision:
            print(f"Found fraudulent behaviour")
        print(f"Time taken to detect fraudulent behaviour: {round(time.time()-start, 4)}")
        self.vector_clock[3]+=1
        self.response = response
        with grpc.insecure_channel('suggestions_service:50053') as channel:
            stub = suggestions_service_grpc.SuggestionsServiceStub(channel)
            vec_clock_msg = suggestions_service.VectorClockInp_sugg()
            vec_clock_msg.vector_clock.extend(self.vector_clock)
            stub.VectorClockUpdate(vec_clock_msg)
    
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