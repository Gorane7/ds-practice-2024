import sys
import os
import random
import time
import threading

# This set of lines are needed to import the gRPC stubs.
# The path of the stubs is relative to the current file, or absolute inside the container.
# Change these lines only if strictly needed.
FILE = __file__ if '__file__' in globals() else os.getenv("PYTHONFILE", "")

utils_path = os.path.abspath(os.path.join(FILE, '../../../utils/pb/database'))
sys.path.insert(0, utils_path)


import database_pb2 as database
import database_pb2_grpc as database_grpc

import grpc
from concurrent import futures


# Create a class to define the server functions, derived from
class Database(database_grpc.DatabaseServicer):
    def __init__(self):
        self.id = int(os.environ['CONTAINER_ID'])
        self.process_amount = int(os.environ['PROCESS_AMOUNT'])
        self.db = {1:4, 2:2} # number of books in stock per book id
        self.lock = {}

    def propagate(self, request, method, crash_on_failure = False):
        peers = set(range(1,self.process_amount))
        while peers:
            for peer in peers.copy():
                with grpc.insecure_channel(f'database_{(self.id+peer)%self.process_amount}:{50105+((self.id+peer)%self.process_amount)}') as channel:
                    stub = database_grpc.DatabaseStub(channel)
                    success = True
                    if method == "write":
                        stub.Write(request)
                    elif method == "lock":
                        resp = stub.Lock(request)
                        success = resp.ok
                    elif method == "release":
                        stub.Release(request)
                    if success:
                        peers.remove(peer)
                    elif crash_on_failure:
                        return resp.other_id
        return 0

    def Read(self, request, context):
        field = request.field
        while field in self.lock:
            time.sleep(0.01)
        response = database.ReadResponse(value=self.db[field])
        return response
    
    def Write(self, request, context):
        field = request.field
        if request.fresh:
            lock_id = time.time()
            done = 0
            while not done:
                self.lock[field] = lock_id
                r = self.propagate(database.LockRequest(field=field, lock_id=lock_id), "lock", crash_on_failure=True)
                if r:
                    self.propagate(database.ReleaseRequest(field=field, lock_id=lock_id), "release")
                    self.lock.pop(field)
                else:
                    done = 1

            self.db[request.field] = request.value
            request.fresh = False
            self.propagate(request, "write")
            self.propagate(database.ReleaseRequest(field=field), "release")
            self.lock.pop(field)
        else:
            self.db[request.field] = request.value
        return database.WriteResponse()

    def Lock(self, request, context):
        field = request.field
        if field in self.lock:
            if self.lock[field] > request.lock_id:
                return database.LockResponse(ok=False, other_id=self.lock[field])
            else:
                while field in self.lock:
                    time.sleep(0.01)
        self.lock[field] = request.lock_id
        return database.LockResponse(ok=True, other_id=-1)

    def Release(self, request, context):
        if request.field in self.lock and self.lock[request.field] == request.lock_id:
            self.lock.pop(request.field)
        return database.ReleaseResponse()



def serve():
    print("Starting doing nothing")
    # Create a gRPC server
    server = grpc.server(futures.ThreadPoolExecutor())
    # Add HelloService
    database_grpc.add_DatabaseServicer_to_server(Database(), server)
    # Listen on port 5010X
    port = str(50105 + int(os.environ['CONTAINER_ID']))
    server.add_insecure_port("[::]:" + port)
    # Start the server
    server.start()
    print(f"Server started. Listening on port {port}.")
    # Keep thread alive
    print(f"Finished doing nothing on port {port}")
    server.wait_for_termination()

if __name__ == '__main__':
    serve()