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
        self.lock = set()
        self.prelock = {}

    def propagate(self, request, method, crash_on_failure = False):
        peers = set(range(1,self.process_amount))
        while peers:
            for peer in peers.copy():
                with grpc.insecure_channel(f'database:{50105+((self.id+peer)%self.process_amount)}') as channel:
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
                        return 1
        return 0

    def Read(self, request, context):
        field = request.field
        while field in self.lock or field in self.prelock:
            time.sleep(0.01)
        response = database.ReadResponse(value=self.db[field])
        return response
    
    def Write(self, request, context):
        field = request.field
        if request.fresh:
            lock_id = time.time()
            res = 1
            while res:
                while field in self.lock or field in self.prelock:
                    time.sleep(0.01)
                self.prelock[field] = lock_id
                self.propagate(database.LockRequest(field=field, preliminary=True, lock_id=lock_id), "lock")
                if self.prelock[field] < lock_id:
                    # prelock was stolen by more important process
                    continue
                elif self.prelock[field] > lock_id:
                    # prelock was stolen by an underling
                    self.prelock[field] = lock_id
                res = self.propagate(database.LockRequest(field=field, preliminary=False, lock_id=lock_id), "lock", crash_on_failure=True)
            self.lock.add(field)
            self.db[request.field] = request.value
            request.fresh = False
            self.propagate(request, "write")
            self.propagate(database.ReleaseRequest(field=field), "release")
            self.lock.remove(field)
        else:
            self.db[request.field] = request.value
        return database.WriteResponse()

    def Lock(self, request, context):
        field = request.field
        pre = request.preliminary
        if pre:
            if field in self.prelock:
                if self.prelock[field] > request.lock_id:
                    self.prelock[field] = request.lock_id
                    return database.LockResponse(ok=True)
                else:
                    return database.LockResponse(ok=False)
            else:
                self.prelock[field] = request.lock_id
                return database.LockResponse(ok=True)
        else:
            if field in self.prelock and self.prelock[field] == request.lock_id:
                self.lock.add(field)
                return database.LockResponse(ok=True)
            else:
                # different higher priority lock has taken this prelocks place
                return database.LockResponse(ok=False)

    def Release(self, request, context):
        self.lock.remove(request.field)
        self.prelock.remove(request.field)
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