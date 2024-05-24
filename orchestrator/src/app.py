import sys
import os
import threading
import time
import random

from tcp_latency import measure_latency


from opentelemetry.sdk.resources import SERVICE_NAME, Resource

from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

from opentelemetry import metrics
from opentelemetry.exporter.otlp.proto.http.metric_exporter import OTLPMetricExporter
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from opentelemetry.metrics import Observation

# This set of lines are needed to import the gRPC stubs.
# The path of the stubs is relative to the current file, or absolute inside the container.
# Change these lines only if strictly needed.
FILE = __file__ if '__file__' in globals() else os.getenv("PYTHONFILE", "")

utils_path = os.path.abspath(os.path.join(FILE, '../../../utils/pb/fraud_detection'))
sys.path.insert(0, utils_path)

utils_path2 = os.path.abspath(os.path.join(FILE, '../../../utils/pb/transaction_verification'))
sys.path.insert(0, utils_path2)

utils_path3 = os.path.abspath(os.path.join(FILE, '../../../utils/pb/suggestions_service'))
sys.path.insert(0, utils_path3)

utils_path4 = os.path.abspath(os.path.join(FILE, '../../../utils/pb/order_queue'))
sys.path.insert(0, utils_path4)

import fraud_detection_pb2 as fraud_detection
import fraud_detection_pb2_grpc as fraud_detection_grpc

import transaction_verification_pb2 as transaction_verification
import transaction_verification_pb2_grpc as transaction_verification_grpc

import suggestions_service_pb2 as suggestions_service
import suggestions_service_pb2_grpc as suggestions_service_grpc

import order_queue_pb2 as order_queue
import order_queue_pb2_grpc as order_queue_grpc

import grpc

def greet(name='you'):
    # Establish a connection with the fraud-detection gRPC service.
    with grpc.insecure_channel('fraud_detection:50051') as channel:
        # Create a stub object.
        stub = fraud_detection_grpc.HelloServiceStub(channel)
        # Call the service through the stub object.
        response = stub.SayHello(fraud_detection.HelloRequest(name=name))
    return response.greeting

def detect_fraud(name='you', req={}, resp={}, order_id=0):
    # Establish a connection with the fraud-detection gRPC service.
    with grpc.insecure_channel('fraud_detection:50051') as channel:
        # Create a stub object.
        stub = fraud_detection_grpc.HelloServiceStub(channel)
        # Call the service through the stub object.
        response = stub.DetectFraud(fraud_detection.FraudRequest(name=name, creditInfo= req["creditCard"], order_id=order_id))
    resp["fraud"] = response.decision
    if response.decision:
        kill_all_services(order_id)
    
def verify_transaction(req={}, resp={}, order_id=0):
    # Establish a connection with the fraud-detection gRPC service.
    with grpc.insecure_channel('transaction_verification:50052') as channel:
        # Create a stub object.
        stub = transaction_verification_grpc.VerifServiceStub(channel)
        # Call the service through the stub object.
        response = stub.Verify(transaction_verification.VerifyRequest(items=req['items'], userInfo=req['user'], creditInfo=req['creditCard'], order_id=order_id))
    resp["verif"] = response.decision
    if response.decision:
        kill_all_services(order_id)
    
def suggest_service(pool=[], ordered_books=[], resp={}, order_id=0):
    # Establish a connection with the fraud-detection gRPC service.
    with grpc.insecure_channel('suggestions_service:50053') as channel:
        # Create a stub object.
        stub = suggestions_service_grpc.SuggestionsServiceStub(channel)
        # Call the service through the stub object.
        response = stub.Suggest(suggestions_service.SuggestionRequest(books=pool, ordered=ordered_books, order_id=order_id))
        res = []
        for book in response.books:
            res.append({"bookId":book.bookId, "title":book.title, "author":book.author})
    resp["suggestions"] = res

def kill_all_services(order_id):
    with grpc.insecure_channel('fraud_detection:50051') as channel:
        stub = fraud_detection_grpc.HelloServiceStub(channel)
        killorder = fraud_detection.KillOrder_fraud(order_id=order_id)
        stub.Kill(killorder)
    with grpc.insecure_channel('transaction_verification:50052') as channel:
        stub = transaction_verification_grpc.VerifServiceStub(channel)
        killorder = transaction_verification.KillOrder_trans(order_id=order_id)
        stub.Kill(killorder)
    with grpc.insecure_channel('suggestions_service:50053') as channel:
        stub = suggestions_service_grpc.SuggestionsServiceStub(channel)
        killorder = suggestions_service.KillOrder_sugg(order_id=order_id)
        stub.Kill(killorder)
        
def enqueue_order(books=[], resp={}):
    # Establish a connection with the order-queue gRPC service.
    with grpc.insecure_channel('order_queue:50054') as channel:
        # Create a stub object.
        stub = order_queue_grpc.OrderQueueStub(channel)
        # Call the service through the stub object.
        response = stub.Enqueue(order_queue.EnqueueRequest(booknames=books))
    resp["enqueue"] = response.success

# Import Flask.
# Flask is a web framework for Python.
# It allows you to build a web application quickly.
# For more information, see https://flask.palletsprojects.com/en/latest/
from flask import Flask, request
from flask_cors import CORS

# Create a simple Flask app.
app = Flask(__name__)
# Enable CORS for the app.
CORS(app)

resource = Resource(attributes={
    SERVICE_NAME: "orchestrator"
})

provider = TracerProvider(resource=resource)
processor = BatchSpanProcessor(OTLPSpanExporter(endpoint="http://observability:4318/v1/traces"))
provider.add_span_processor(processor)
trace.set_tracer_provider(provider)

# Creates a tracer from the global tracer provider
tracer = trace.get_tracer("checkout.tracer")


metric_reader = PeriodicExportingMetricReader(OTLPMetricExporter("http://observability:4318/v1/metrics"))
meter_provider = MeterProvider(metric_readers=[metric_reader], resource=resource)
metrics.set_meter_provider(meter_provider)
meter = metrics.get_meter("orchestrator.requests.meter")

active_request_counter = meter.create_up_down_counter(name="active.requests.counter", description="The number of active requests")


request_duration = meter.create_histogram(
    name="orchestrator.request.duration",
    description="Measures the duration of the request",
    unit="ms")

global last_request_time
last_request_time = time.time()

def latency_test(arg):
    target = "neti.ee"
    try:
        val = measure_latency(host=target)[0]
    except:
        val = 10000
    print(f"Latency to '{target}' was {round(val, 2)} ms")
    yield Observation(val, {})

def time_since_last_request(arg):
    global last_request_time
    time_since = time.time() - last_request_time
    print(f"Time since last request is {round(time_since, 2)} s")
    yield Observation(time_since, {})

meter.create_observable_gauge("network.latency", [latency_test])
meter.create_observable_gauge("orchestrator.time.since.last.request", [time_since_last_request])


# Define a GET endpoint.
@app.route('/', methods=['GET'])
def index():
    """
    Responds with 'Hello, [name]' when a GET request is made to '/' endpoint.
    """
    # Test the fraud-detection gRPC service.
    response = greet(name='orchestrator')
    # Return the response.
    return response

@app.route('/checkout', methods=['POST'])
def checkout():
    """
    Responds with a JSON object containing the order ID, status, and suggested books.
    """
    global last_request_time
    start = time.time()
    last_request_time = start
    active_request_counter.add(1)
    with tracer.start_as_current_span("checkout-span") as span:
        # Print request object data
        order_id = int(random.random()*8008135420)
        span.set_attribute("checkout.order_id", order_id)
        print(f"Order ID {order_id} has request Data:", request.json)

        pool=[
                {'bookId': '1', 'title': 'Learning Python', 'author': 'John Smith'},
                {'bookId': '2', 'title': 'JavaScript - The Good Parts', 'author': 'Jane Doe'},
                {'bookId': '3', 'title': 'Domain-Driven Design: Tackling Complexity in the Heart of Software', 'author': 'Eric Evans'},
                {'bookId': '4', 'title': 'Design Patterns: Elements of Reusable Object-Oriented Software', 'author': 'Erich Gamma, Richard Helm, Ralph Johnson, & John Vlissides'}
            ]
        book_names = [x["name"] for x in request.json["items"]]
        
        responses = {}

    
    fraud_thread = threading.Thread(target=detect_fraud, kwargs={"name":request.json["user"]["name"], "req":request.json, "resp": responses, "order_id":order_id})
    verif_thread = threading.Thread(target=verify_transaction, kwargs={"req":request.json, "resp": responses, "order_id":order_id})
    suggestion_thread = threading.Thread(target=suggest_service, kwargs={"pool":pool, "ordered_books":book_names, "resp": responses, "order_id":order_id})
    fraud_thread.start()
    verif_thread.start()
    suggestion_thread.start()
    fraud_thread.join()
    verif_thread.join()
    suggestion_thread.join()
    

    decision = responses["fraud"]
    trans_verif = responses["verif"]
    suggestions = responses["suggestions"]

    print(f"Fraud decision: {decision}")
    print(f"Transaction verification: {trans_verif}")
    
    span.set_attribute("checkout.fraud_decision", decision)
    span.set_attribute("checkout.transaction_verification", trans_verif)
    span.set_attribute("checkout.book_suggestions", suggestions)

    if not decision and not trans_verif:
        enqueue_thread = threading.Thread(target=enqueue_order, kwargs={"books": book_names, "resp": responses})
        enqueue_thread.start()
        enqueue_thread.join()

    # Dummy response following the provided YAML specification for the bookstore
    order_status_response = {
        'orderId': order_id,
        'status': 'Fraud detected' if decision else ("Incorrect transaction details (credit card number, name etc)" if trans_verif else "Order accepted"),
        'suggestedBooks': suggestions
    }

    active_request_counter.add(-1)
    request_duration.record(1000 * (time.time() - start))
    return order_status_response


if __name__ == '__main__':
    # Run the app in debug mode to enable hot reloading.
    # This is useful for development.
    # The default port is 5000.
    app.run(host='0.0.0.0')
