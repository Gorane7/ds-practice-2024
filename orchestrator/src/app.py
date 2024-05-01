import sys
import os
import threading
import time
import random

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

utils_path5 = os.path.abspath(os.path.join(FILE, '../../../utils/pb/database'))
sys.path.insert(0, utils_path5)

import fraud_detection_pb2 as fraud_detection
import fraud_detection_pb2_grpc as fraud_detection_grpc

import transaction_verification_pb2 as transaction_verification
import transaction_verification_pb2_grpc as transaction_verification_grpc

import suggestions_service_pb2 as suggestions_service
import suggestions_service_pb2_grpc as suggestions_service_grpc

import order_queue_pb2 as order_queue
import order_queue_pb2_grpc as order_queue_grpc

import database_pb2 as database
import database_pb2_grpc as database_grpc

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

def query_db(book_id, resp={}):
    # pick random database instance to balance the load somewhat evenly
    db_id = random.randint(0,3)
    with grpc.insecure_channel(f'database:{50105+db_id}') as channel:
        # Create a stub object.
        stub = database_grpc.DatabaseStub(channel)
        # Call the service through the stub object.
        response = stub.Read(database.ReadRequest(field=book_id))
    return response.value
    
def update_db(book_id, value, resp={}):
    # pick random database instance to balance the load somewhat evenly
    db_id = random.randint(0,3)
    with grpc.insecure_channel(f'database:{50105+db_id}') as channel:
        # Create a stub object.
        stub = database_grpc.DatabaseStub(channel)
        # Call the service through the stub object.
        response = stub.Write(database.WriteRequest(field=book_id, value=value, fresh=True))

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
    # Print request object data
    order_id = int(random.random()*8008135420)
    print("Request Data:", request.json)

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

    for book in request.json["items"]:
        book_stock = query_db(book["bookId"])
        print(f"There are {book_stock} copies of the book {book['name']} remaining")
        # might want to do something here if stock is 0
        update_db(book["bookId"], book_stock-1)

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

    return order_status_response


if __name__ == '__main__':
    # Run the app in debug mode to enable hot reloading.
    # This is useful for development.
    # The default port is 5000.
    app.run(host='0.0.0.0')
