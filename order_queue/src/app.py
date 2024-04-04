import sys
import os
import random
import time


# This set of lines are needed to import the gRPC stubs.
# The path of the stubs is relative to the current file, or absolute inside the container.
# Change these lines only if strictly needed.
FILE = __file__ if '__file__' in globals() else os.getenv("PYTHONFILE", "")
utils_path = os.path.abspath(os.path.join(FILE, '../../../utils/pb/order_queue'))
sys.path.insert(0, utils_path)
import order_queue_pb2 as order_queue
import order_queue_pb2_grpc as order_queue_grpc

import grpc
from concurrent import futures


# Create a class to define the server functions, derived from
# order_queue_pb2_grpc.OrderQueueServicer
class OrderQueue(order_queue_grpc.OrderQueueServicer):

    def __init__(self):
        self.queue = []
    
    def Enqueue(self, request, context):
        self.queue.append(request.booknames)
        response = order_queue.EnqueueResponse(success=True)
        print(f"Order {request.booknames} was enqueued successfully")
        return response

    def Dequeue(self, request, context):
        if not self.queue:
            response = order_queue.DequeueResponse(booknames=[], have_order=False)
            print(f"Did not have any orders queued")
            return response
        response = order_queue.DequeueResponse(booknames=self.queue.pop(), have_order=True)
        print(f"Order {response.booknames} was successfully dequeued")
        return response

def serve():
    # Create a gRPC server
    server = grpc.server(futures.ThreadPoolExecutor())
    # Add HelloService
    order_queue_grpc.add_OrderQueueServicer_to_server(OrderQueue(), server)
    # Listen on port 50054
    port = "50054"
    server.add_insecure_port("[::]:" + port)
    # Start the server
    server.start()
    print("Server started. Listening on port 50054.")
    # Keep thread alive
    server.wait_for_termination()

if __name__ == '__main__':
    serve()