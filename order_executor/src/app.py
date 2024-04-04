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
        
        # Start a thread to periodically send requests to OrderQueue service
        self.periodic_request_thread = threading.Thread(target=self.send_periodic_request)
        self.periodic_request_thread.daemon = True
        self.periodic_request_thread.start()
    
    def send_periodic_request(self):
        while True:
            # Define your request here
            request = order_queue.DequeueRequest()
            
            # Send request to OrderQueue service
            response = self.stub.Dequeue(request)
            if response.have_order:
                print(f"Executing order {response.booknames}")
            else:
                print(f"Did not have order to execute")

            # Sleep for some time before sending the next request
            time.sleep(10)  # Sleep for 10 seconds, adjust as needed

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