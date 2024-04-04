import sys
import os
import re
import datetime
import time
import threading

# This set of lines are needed to import the gRPC stubs.
# The path of the stubs is relative to the current file, or absolute inside the container.
# Change these lines only if strictly needed.
FILE = __file__ if '__file__' in globals() else os.getenv("PYTHONFILE", "")
utils_path = os.path.abspath(os.path.join(FILE, '../../../utils/pb/transaction_verification'))
sys.path.insert(0, utils_path)
import transaction_verification_pb2 as transaction_verification
import transaction_verification_pb2_grpc as transaction_verification_grpc

utils_path = os.path.abspath(os.path.join(FILE, '../../../utils/pb/fraud_detection'))
sys.path.insert(0, utils_path)

import fraud_detection_pb2 as fraud_detection
import fraud_detection_pb2_grpc as fraud_detection_grpc

import grpc
from concurrent import futures

# Create a class to define the server functions, derived from
# transaction_verification_pb2_grpc.HelloServiceServicer
class VerifService(transaction_verification_grpc.VerifServiceServicer):
    def __init__(self):
        self.vector_clock = [0,0,0,0,0]
        self.request = None
        self.response = None
        self.part1dep = [0,0,0,0,0]
        self.part2dep = [0,0,0,0,0]

    def VectorClockUpdate(self, request, context):
        self.vector_clock = [max(self.vector_clock[i], request.vector_clock[i]) for i in range(len(self.vector_clock))]
        return transaction_verification.Empty_trans()

    # Create an RPC function to say hello
    def Verify(self, request, context):
        self.request = request
        thread1 = threading.Thread(target=self.verifyPart1)
        thread2 = threading.Thread(target=self.verifyPart2)
        thread1.start()
        thread2.start()
        thread1.join()
        thread2.join()
        return self.response
    
    def verifyPart1(self):
        while not self.depCheck(self.vector_clock,self.part1dep):
            time.sleep(0.1)
        request = self.request
        start = time.time()
        response = transaction_verification.VerifyResponse()
        response.decision = 0
        if len(request.items) == 0:
            response.decision ^= (1<<1)
            print("Transaction failure: empty list of items")
        if request.userInfo.name == "":
            response.decision ^= (1<<2)
            print("Transaction failure: empty client name")
        if request.userInfo.contact == "":
            response.decision ^= (1<<3)
            print("Transaction failure: empty client contact info")
        if request.creditInfo.number == "":
            response.decision ^= (1<<4)
            print("Transaction failure: empty credit card number")
        if not request.creditInfo.number.isnumeric():
            response.decision ^= (1<<5)
            print("Transaction failure: non numeric credit card number")
        if not re.match("^(0[0-9]|10|11|12)/[0-9][0-9]$", request.creditInfo.expirationDate):
            response.decision ^= (1<<6)
            print("Transaction failure: credit card expiration date not legal date")
        month = int(request.creditInfo.expirationDate[:2])
        year = int(request.creditInfo.expirationDate[3:])
        if year < datetime.datetime.now().year%100 or year == datetime.datetime.now().year%100 and month < datetime.datetime.now().month:
            response.decision ^= (1<<7)
            print("Transaction failure: credit card expired")
        if len(request.creditInfo.cvv) <3:
            response.decision ^= (1<<8)
            print("Transaction failure: credit card CVV number too short")
        if len(request.creditInfo.cvv) > 4:
            response.decision ^= (1<<9)
            print("Transaction failure: credit card CVV number too long")
        if not request.creditInfo.cvv.isnumeric():
            response.decision ^= (1<<10)
            print("Transaction failure: credit card CVV number non numeric")
        print(f"Bitmap of transaction verification results: {response.decision}")
        print(f"Time taken to verify transaction {round(time.time()-start, 4)}")
        self.response = response
        self.vector_clock[0]+=1
        with grpc.insecure_channel('fraud_detection:50051') as channel:
            stub = fraud_detection_grpc.HelloServiceStub(channel)
            vec_clock_msg = fraud_detection.VectorClockInp_fraud()
            vec_clock_msg.vector_clock.extend(self.vector_clock)
            stub.VectorClockUpdate(vec_clock_msg)

    def verifyPart2(self):
        while not self.depCheck(self.vector_clock,self.part2dep):
            time.sleep(0.1)
        request = self.request
        start = time.time()
        response = transaction_verification.VerifyResponse()
        response.decision = 0
        if len(request.items) == 0:
            response.decision ^= (1<<1)
            print("Transaction failure: empty list of items")
        if request.userInfo.name == "":
            response.decision ^= (1<<2)
            print("Transaction failure: empty client name")
        if request.userInfo.contact == "":
            response.decision ^= (1<<3)
            print("Transaction failure: empty client contact info")
        if request.creditInfo.number == "":
            response.decision ^= (1<<4)
            print("Transaction failure: empty credit card number")
        if not request.creditInfo.number.isnumeric():
            response.decision ^= (1<<5)
            print("Transaction failure: non numeric credit card number")
        if not re.match("^(0[0-9]|10|11|12)/[0-9][0-9]$", request.creditInfo.expirationDate):
            response.decision ^= (1<<6)
            print("Transaction failure: credit card expiration date not legal date")
        month = int(request.creditInfo.expirationDate[:2])
        year = int(request.creditInfo.expirationDate[3:])
        if year < datetime.datetime.now().year%100 or year == datetime.datetime.now().year%100 and month < datetime.datetime.now().month:
            response.decision ^= (1<<7)
            print("Transaction failure: credit card expired")
        if len(request.creditInfo.cvv) <3:
            response.decision ^= (1<<8)
            print("Transaction failure: credit card CVV number too short")
        if len(request.creditInfo.cvv) > 4:
            response.decision ^= (1<<9)
            print("Transaction failure: credit card CVV number too long")
        if not request.creditInfo.cvv.isnumeric():
            response.decision ^= (1<<10)
            print("Transaction failure: credit card CVV number non numeric")
        print(f"Bitmap of transaction verification results: {response.decision}")
        print(f"Time taken to verify transaction {round(time.time()-start, 4)}")
        self.response = response
        self.vector_clock[1]+=1
        with grpc.insecure_channel('fraud_detection:50051') as channel:
            stub = fraud_detection_grpc.HelloServiceStub(channel)
            vec_clock_msg = fraud_detection.VectorClockInp_fraud()
            vec_clock_msg.vector_clock.extend(self.vector_clock)
            stub.VectorClockUpdate(vec_clock_msg)


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