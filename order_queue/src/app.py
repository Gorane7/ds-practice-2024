import sys
import os
import random
import time

import queue

from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry import metrics
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader

from opentelemetry.exporter.otlp.proto.http.metric_exporter import OTLPMetricExporter


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


resource = Resource(attributes={
    SERVICE_NAME: "order_queue"
})

metric_reader = PeriodicExportingMetricReader(OTLPMetricExporter("http://observability:4318/v1/metrics"))
meter_provider = MeterProvider(metric_readers=[metric_reader], resource=resource)
metrics.set_meter_provider(meter_provider)
meter = metrics.get_meter("order.queue.meter")

queue_counter = meter.create_up_down_counter(name="queue.counter", description="The number of orders in a queue")


# Create a class to define the server functions, derived from
# order_queue_pb2_grpc.OrderQueueServicer
class OrderQueue(order_queue_grpc.OrderQueueServicer):

    def __init__(self):
        self.queue = queue.PriorityQueue()
    
    def Enqueue(self, request, context):
        self.queue.put((request.priority, request.booknames))
        queue_counter.add(1)
        response = order_queue.EnqueueResponse(success=True)
        print(f"Order {request.booknames} was enqueued with priority {request.priority} successfully")
        return response

    def Dequeue(self, request, context):
        try:
            priority, booknames = self.queue.get(block=False)
            response = order_queue.DequeueResponse(booknames=booknames, have_order=True)
            print(f"Order {response.booknames} was successfully dequeued with priority {priority}")
            queue_counter.add(-1)
            return response
        except:
            response = order_queue.DequeueResponse(booknames=[], have_order=False)
            #print(f"Did not have any orders queued")
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