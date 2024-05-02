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

utils_path2 = os.path.abspath(os.path.join(FILE, '../../../utils/pb/database'))
sys.path.insert(0, utils_path2)

import order_queue_pb2 as order_queue
import order_queue_pb2_grpc as order_queue_grpc

import order_executor_pb2 as order_executor
import order_executor_pb2_grpc as order_executor_grpc

import database_pb2 as database
import database_pb2_grpc as database_grpc

import grpc
from concurrent import futures


def query_db(book_id, resp={}):
    # pick random database instance to balance the load somewhat evenly
    db_id = random.randint(0,3)
    with grpc.insecure_channel(f'database_{db_id}:{50105+db_id}') as channel:
        # Create a stub object.
        stub = database_grpc.DatabaseStub(channel)
        # Call the service through the stub object.
        response = stub.Read(database.ReadRequest(field=book_id))
    return response.value
    
def update_db(book_id, value, resp={}):
    # pick random database instance to balance the load somewhat evenly
    db_id = random.randint(0,3)
    with grpc.insecure_channel(f'database_{db_id}:{50105+db_id}') as channel:
        # Create a stub object.
        stub = database_grpc.DatabaseStub(channel)
        # Call the service through the stub object.
        response = stub.Write(database.WriteRequest(field=book_id, value=value, fresh=True))


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
        self.next_id = (self.id + 1) % self.process_amount
        self.busy = False
        self.operational = True
        self.last_token_seen = time.time()
        self.sleep_time = 0.5
        self.panic_coefficient = 3
        self.process_time = 5
        
        # Start a thread to periodically send requests to OrderQueue service
        self.periodic_request_thread = threading.Thread(target=self.send_periodic_request)
        self.periodic_request_thread.daemon = True
        self.periodic_request_thread.start()

        # TODO: If executor starts before queue, then it crashes currently
    
    def send_periodic_request(self):
        # Wait for others to wake up
        time.sleep(5)
        self.last_token_seen = time.time()
        
        while True:
            if self.operational:
                if random.random() < 0: #0.01:
                    self.operational = False
                    print(f"ERROR: Crash and burn")
            else:
                if random.random() < 0.1:
                    self.operational = True
                    print(f"SUCCESS: Came back to life")
            time.sleep(self.sleep_time)
            if not self.operational:
                continue
            if self.token:
                self.last_token_seen = time.time()
                if not self.busy:
                    #print("Asking for orders")
                    request = order_queue.DequeueRequest()
                    response = self.stub.Dequeue(request)
                    if response.have_order:
                        #print("Got orders")
                        threading.Thread(target=self.process_request, args=(response.booknames, )).start()
                    else:
                        pass
                        #print(f"Did not have order to execute")
                self.send_token(self.next_id)
            else:
                if time.time() - self.last_token_seen > self.sleep_time * self.process_amount * self.panic_coefficient:
                    self.ask_restart()
    
    def process_request(self, booknames):
        self.busy = True
        print(f"Starting processing of {booknames}")
        
        for book in booknames:
            book_stock = query_db(book)
            print(f"There are {book_stock} copies of the book {book} remaining")
            # might want to do something here if stock is 0
            # We might want to fail the commit in that case
            update_db(book, book_stock - 1)
        
        print(f"Finished processing of {booknames}")
        self.busy = False
    
    def send_token(self, remote_id):
        #print(f"{self.id} sending token to {remote_id}")
        self.token = False
        try:
            with grpc.insecure_channel(f"order_executor_{remote_id}:{50100 + remote_id}") as channel:
                stub = order_executor_grpc.OrderExecutorStub(channel)
                request = order_executor.TokenRequest()
                response = stub.Token(request)
        except Exception as e:
            #print("Got error: " + str(e))
            print("Failed to send away token, taking it back")
            self.token = True
            self.next_id = (self.next_id + 1) % self.process_amount
        
    def ask_restart(self):
        print("Haven't seen token in a while, asking to be let back in the ring")
        previous = (self.id - 1) % self.process_amount
        while True:
            try:
                with grpc.insecure_channel(f"order_executor_{previous}:{50100 + previous}") as channel:
                    stub = order_executor_grpc.OrderExecutorStub(channel)
                    request = order_executor.RestartRequest(restarter_id=self.id)
                    response = stub.Restart(request)
                    # When getting restartrequest, then check if current next id is smaller than the person asking for a restart, if is, then tell him to restart the restart
                    if not response.restart_success:
                        previous = (self.id - 1) % self.process_amount
                    break
            except Exception as e:
                print(e)
                previous = (self.id - 1) % self.process_amount
        self.next_id = response.next_id
        self.last_token_seen = time.time()
    
    def Restart(self, request, context):
        print(f"{request.restarter_id} asked to be let back in the ring")
        if self.id == self.next_id:
            print(f"Node was alone in the ring, adding other")
            response = order_executor.RestartResponse(next_id=self.id, restart_success=True)
            self.next_id = request.restarter_id
            return response
        # Order in rings modulo N is complicated
        if not (self.id < request.restarter_id < self.next_id or request.restarter_id < self.next_id < self.id or self.next_id < self.id < request.restarter_id):
            response = order_executor.RestartResponse(next_id=request.restarter_id, restart_success=False)
            return response
        print(f"Telling {request.restarter_id} to send token to {self.next_id} and starting to send myself to {request.restarter_id}")
        response = order_executor.RestartResponse(next_id=self.next_id, restart_success=True)
        self.next_id = request.restarter_id
        return response
    
    
    def Token(self, request, context):
        if not self.operational:
            return
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