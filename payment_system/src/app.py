import sys
import os
import re
import datetime
import time
import threading
import random
from collections import defaultdict

# This set of lines are needed to import the gRPC stubs.
# The path of the stubs is relative to the current file, or absolute inside the container.
# Change these lines only if strictly needed.
FILE = __file__ if '__file__' in globals() else os.getenv("PYTHONFILE", "")


import grpc
from concurrent import futures

utils_path = os.path.abspath(os.path.join(FILE, '../../../utils/pb/payment_system'))
sys.path.insert(0, utils_path)

import payment_system_pb2 as payment_system
import payment_system_pb2_grpc as payment_system_grpc

# Create a class to define the server functions, derived from
class PaymentSystem(payment_system_grpc.PaymentSystemServicer):
    def __init__(self):
        self.to_commit = {}
    
    def StartPayment(self, request, context):
        if self.has_money(request.credit_card, request.amount):
            self.reserve_money(request.credit_card, request.amount)
            self.to_commit[request.payment_id] = (request.credit_card, request.amount)
            print(f"Created reservation with ID {request.payment_id} for card {request.credit_card} equal to {request.amount} money")
            return payment_system.PaymentResponse(success=True)
        print(f"Card {request.credit_card} did not have {request.amount} money, unable to create reservation")
        return payment_system.PaymentResponse(success=False)
    
    def ConfirmPayment(self, request, context):
        if request.payment_id not in self.to_commit.keys():
            print(f"Never made reservation with ID {request.payment_id}, so rollback unnecessary")
            return payment_system.PaymentResponse(success=True)
        
        credit_card, amount = self.to_commit[request.payment_id]
        if request.perform_payment:
            self.make_payment(credit_card, amount)
        else:
            self.release_payment(credit_card, amount)
            
        del self.to_commit[request.payment_id]
        print(f"Removed reservation of {amount} money with ID {request.payment_id} from card {credit_card}")
        
        return payment_system.PaymentResponse(success=True)
    
    def reserve_money(self, credit_card, amount):
        print(f"Reserving {amount} money on card {credit_card}")
    
    def make_payment(self, credit_card, amount):
        print(f"Making payment of {amount} money from card {credit_card}")
        
    def release_payment(self, credit_card, amount):
        print(f"Releasing payment of {amount} money from card {credit_card}")
    
    def has_money(self, credit_card, amount):
        return sum([int(x) for x in str(credit_card)]) > amount


def serve():
    # Create a gRPC server
    server = grpc.server(futures.ThreadPoolExecutor())
    # Add PaymentSystem
    payment_system_grpc.add_PaymentSystemServicer_to_server(PaymentSystem(), server)
    # Listen on port 50055
    port = "50055"
    server.add_insecure_port("[::]:" + port)
    # Start the server
    server.start()
    print("Server started. Listening on port 50055.")
    # Keep thread alive
    server.wait_for_termination()

if __name__ == '__main__':
    serve()