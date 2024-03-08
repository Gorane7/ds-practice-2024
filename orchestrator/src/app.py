import sys
import os

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
import fraud_detection_pb2 as fraud_detection
import fraud_detection_pb2_grpc as fraud_detection_grpc
import transaction_verification_pb2 as transaction_verification
import transaction_verification_pb2_grpc as transaction_verification_grpc
import suggestions_service_pb2 as suggestions_service
import suggestions_service_pb2_grpc as suggestions_service_grpc

import grpc

def greet(name='you'):
    # Establish a connection with the fraud-detection gRPC service.
    with grpc.insecure_channel('fraud_detection:50051') as channel:
        # Create a stub object.
        stub = fraud_detection_grpc.HelloServiceStub(channel)
        # Call the service through the stub object.
        response = stub.SayHello(fraud_detection.HelloRequest(name=name))
    return response.greeting

def detect_fraud(name='you'):
    # Establish a connection with the fraud-detection gRPC service.
    with grpc.insecure_channel('fraud_detection:50051') as channel:
        # Create a stub object.
        stub = fraud_detection_grpc.HelloServiceStub(channel)
        # Call the service through the stub object.
        response = stub.DetectFraud(fraud_detection.FraudRequest(name=name)) 
    return response.decision
    
def verify_transaction(req={}):
    # Establish a connection with the fraud-detection gRPC service.
    with grpc.insecure_channel('transaction_verification:50052') as channel:
        # Create a stub object.
        stub = transaction_verification_grpc.VerifServiceStub(channel)
        # Call the service through the stub object.
        response = stub.Verify(transaction_verification.VerifyRequest(items=req['items'], userInfo=req['user'], creditInfo=req['creditCard']))
    return response.decision
    
def suggest_service(pool=[], ordered_books=[]):
    # Establish a connection with the fraud-detection gRPC service.
    with grpc.insecure_channel('suggestions_service:50053') as channel:
        # Create a stub object.
        stub = suggestions_service_grpc.SuggestionsServiceStub(channel)
        # Call the service through the stub object.
        response = stub.Suggest(suggestions_service.SuggestionRequest(books=pool, ordered=ordered_books))
        res = []
        for book in response.books:
            res.append({"bookId":book.bookId, "title":book.title, "author":book.author})
    return res

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
    print("Request Data:", request.json)

    decision = detect_fraud(name=request.json["user"]["name"])
    print(f"Decision was {decision}")

    trans_verif = verify_transaction(req=request.json)
    print(f"Transaction verification result: {trans_verif}")

    book_names = [x["name"] for x in request.json["items"]]

    suggestions = suggest_service(
        pool=[
            {'bookId': '1', 'title': 'Learning Python', 'author': 'John Smith'},
            {'bookId': '2', 'title': 'JavaScript - The Good Parts', 'author': 'Jane Doe'},
            {'bookId': '3', 'title': 'Domain-Driven Design: Tackling Complexity in the Heart of Software', 'author': 'Eric Evans'},
            {'bookId': '4', 'title': 'Design Patterns: Elements of Reusable Object-Oriented Software', 'author': 'Erich Gamma, Richard Helm, Ralph Johnson, & John Vlissides'}
        ],
        ordered_books=book_names
    )

    # Dummy response following the provided YAML specification for the bookstore
    order_status_response = {
        'orderId': '12345',
        'status': 'Order Approved' if decision else 'Fraud detected' if trans_verif else "Incorrect transaction details (credit card number, name etc)",
        'suggestedBooks': suggestions
    }

    return order_status_response


if __name__ == '__main__':
    # Run the app in debug mode to enable hot reloading.
    # This is useful for development.
    # The default port is 5000.
    app.run(host='0.0.0.0')
