import sys
import os
import re

# This set of lines are needed to import the gRPC stubs.
# The path of the stubs is relative to the current file, or absolute inside the container.
# Change these lines only if strictly needed.
FILE = __file__ if '__file__' in globals() else os.getenv("PYTHONFILE", "")
utils_path = os.path.abspath(os.path.join(FILE, '../../../utils/pb/transaction_verification'))
sys.path.insert(0, utils_path)
import transaction_verification_pb2 as transaction_verification
import transaction_verification_pb2_grpc as transaction_verification_grpc

import grpc
from concurrent import futures

# Create a class to define the server functions, derived from
# transaction_verification_pb2_grpc.HelloServiceServicer
class VerifService(transaction_verification_grpc.VerifServiceServicer):
    # Create an RPC function to say hello
    '''
    def SayHello(self, request, context):
        # Create a HelloResponse object
        response = transaction_verification.HelloResponse()
        # Set the greeting field of the response object
        response.greeting = "Hello, " + request.name
        # Print the greeting message
        print(response.greeting)
        # Return the response object
        return response
        '''
    
    def Verify(self, request, context):
        response = transaction_verification.VerifyResponse()
        response.decision = True
        if len(request.items) == 0:
            response.decision = False
            print(1)
        elif request.userInfo.name == "" or request.userInfo.contact == "":
            response.decision = False
            print(2)
        elif request.creditInfo.number == "" or not request.creditInfo.number.isnumeric() or not re.match("^(0[0-9]|10|11|12)/[0-9][0-9]$", request.creditInfo.expirationDate) or len(request.creditInfo.cvv) <3 or len(request.creditInfo.cvv) > 4 or not request.creditInfo.cvv.isnumeric():
            response.decision = False
            print(3)
        print(response.decision)
        return response

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