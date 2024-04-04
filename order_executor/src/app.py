import sys
import os
import random
import time
import threading

# This set of lines are needed to import the gRPC stubs.
# The path of the stubs is relative to the current file, or absolute inside the container.
# Change these lines only if strictly needed.
FILE = __file__ if '__file__' in globals() else os.getenv("PYTHONFILE", "")

utils_path = os.path.abspath(os.path.join(FILE, '../../../utils/pb/order_queue'))
sys.path.insert(0, utils_path)

utils_path1 = os.path.abspath(os.path.join(FILE, '../../../utils/pb/order_executor'))
sys.path.insert(0, utils_path1)

import order_queue_pb2 as order_queue
import order_queue_pb2_grpc as order_queue_grpc

import order_executor_pb2 as order_executor
import order_executor_pb2_grpc as order_executor_grpc

import grpc
from concurrent import futures


# Create a class to define the server functions, derived from
# order_executor_pb2_grpc.OrderExecutorServicer
class OrderExecutor(order_executor_grpc.OrderExecutorServicer):
    def __init__(self):
        # Initialize a gRPC channel to communicate with OrderQueue service
        self.channel = grpc.insecure_channel(f'order_queue:50054')
        self.stub = order_queue_grpc.OrderQueueStub(self.channel)

        self.id = int(os.environ['CONTAINER_ID'])
        self.process_amount = int(os.environ['PROCESS_AMOUNT'])
        self.token = self.id == 0
        self.busy = False
        
        # Start a thread to periodically send requests to OrderQueue service
        self.periodic_request_thread = threading.Thread(target=self.send_periodic_request)
        self.periodic_request_thread.daemon = True
        self.periodic_request_thread.start()
    
    def send_periodic_request(self):
        while True:
            time.sleep(1)
            if self.token:
                if not self.busy:
                    print("Asking for orders")
                    request = order_queue.DequeueRequest()
                    response = self.stub.Dequeue(request)
                    if response.have_order:
                        print("Got orders")
                        threading.Thread(target=self.process_request, args=(response.booknames, )).start()
                    else:
                        print(f"Did not have order to execute")
                self.send_token((self.id + 1) % self.process_amount)
    
    def process_request(self, booknames):
        self.busy = True
        print(f"Starting processing of {booknames}")
        time.sleep(random.random() * 10 + 10)
        print(f"Finished processing of {booknames}")
        self.busy = False
    
    def send_token(self, remote_id):
        self.token = False
        print(f"Sending away token to {remote_id}")
        try:
            with grpc.insecure_channel(f"order_executor_{remote_id}:{50100 + remote_id}") as channel:
                stub = order_executor_grpc.OrderExecutorStub(channel)
                request = order_executor.TokenRequest()
                response = stub.Token(request)
        except Exception as e:
            print("Got error: " + str(e))
            print("Failed to send away token, taking it back")
            self.token = True
    
    def Token(self, request, context):
        print("Received token")
        self.token = True
        response = order_executor.TokenResponse()
        return response



def serve():
    print("Starting doing nothing")
    # Create a gRPC server
    server = grpc.server(futures.ThreadPoolExecutor())
    # Add HelloService
    order_executor_grpc.add_OrderExecutorServicer_to_server(OrderExecutor(), server)
    # Listen on port 5010X
    port = str(50100 + int(os.environ['CONTAINER_ID']))
    server.add_insecure_port("[::]:" + port)
    # Start the server
    server.start()
    print(f"Server started. Listening on port {port}.")
    # Keep thread alive
    print(f"Finished doing nothing on port {port}")
    server.wait_for_termination()

if __name__ == '__main__':
    serve()