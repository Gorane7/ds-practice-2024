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
        self.db = {
            "Learning Python": 4, 
            "JavaScript - The Good Parts": 2,
            "Domain-Driven Design: Tackling Complexity in the Heart of Software": 10,
            "Design Patterns: Elements of Reusable Object-Oriented Software": 5
        } # number of books in stock per book id
        self.modifications = {}
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
                    elif method == "modify":
                        stub.Modify(request)
                        
                    if success:
                        peers.remove(peer)
                    elif crash_on_failure:
                        return False
        return True

    def Read(self, request, context):
        field = request.field
        while field in self.lock:
            time.sleep(0.01)
        response = database.ReadResponse(value=self.db[field])
        return response
    
    def Write(self, request, context):
        field = request.field
        if not request.fresh:
            self.db[field] = request.value
            return database.WriteResponse()

        lock_id = int(time.time() * 1000)
        while True:
            while field in self.lock:
                time.sleep(0.01)
            self.lock[field] = lock_id
            print(f"Locked field {field} with {lock_id} because of Write")
            if self.propagate(database.LockRequest(field=field, lock_id=lock_id), "lock", crash_on_failure=True):
                break
            
            self.propagate(database.ReleaseRequest(field=field, lock_id=lock_id), "release")
            self.lock.pop(field)
            print(f"Released field {field} from Write")
            time.sleep(0.01)

        self.db[field] = request.value
        request.fresh = False
        
        self.propagate(request, "write")
        self.propagate(database.ReleaseRequest(field=field, lock_id=lock_id), "release")
        
        self.lock.pop(field)
        print(f"Released field {field} from Write")
        return database.WriteResponse()
    
    def Modify(self, request, context):
        field = request.field
        if not request.fresh:
            self.db[field] += request.value
            self.modifications[request.modify_id] = (field, request.value)
            return database.ModifyResponse(success=True)

        lock_id = int(time.time() * 1000)
        while True:
            self.lock[field] = lock_id
            print(f"Locked field {field} with {lock_id} because of Modify")
            if self.propagate(database.LockRequest(field=field, lock_id=lock_id), "lock", crash_on_failure=True):
                break
            
            self.propagate(database.ReleaseRequest(field=field, lock_id=lock_id), "release")
            self.lock.pop(field)
            print(f"Released field {field} from Modify")
            time.sleep(0.01)

        self.db[field] += request.value
        self.modifications[request.modify_id] = (field, request.value)
        request.fresh = False
        
        self.propagate(request, "modify")
        self.propagate(database.ReleaseRequest(field=field, lock_id=lock_id), "release")
        
        self.lock.pop(field)
        print(f"Released field {field} from Modify")
        return database.ModifyResponse(success=True)
    
    def ModifyCommit(self, request, context):
        if not request.fresh:
            if request.to_commit:
                del self.modifications[request.modify_id]
            else:
                field, value = self.modifications[request.modify_id]
                self.db[field] -= value
                del self.modifications[request.modify_id]
            return database.ModifyCommitResponse()
        
        if request.to_commit:
            del self.modifications[request.modify_id]
            self.propagate(database.ModifyCommitRequest(to_commit=True, modify_id=request.modify_id, fresh=False))
            return database.ModifyCommitResponse()
        
        field, value = self.modifications[request.modify_id]
        lock_id = int(time.time() * 1000)
        while True:
            self.lock[field] = lock_id
            print(f"Locked field {field} with {lock_id} because of ModifyCommit rollback")
            if self.propagate(database.LockRequest(field=field, lock_id=lock_id), "modify-commit", crash_on_failure=True):
                break
            
            self.propagate(database.ReleaseRequest(field=field, lock_id=lock_id), "release")
            self.lock.pop(field)
            print(f"Released field {field} from ModifyCommit")
            time.sleep(0.01)
        
        self.db[field] -= value
        del self.modifications[request.modify_id]
        request.fresh = False
        
        self.propagate(request, "modify-commit")
        self.propagate(database.ReleaseRequest(field=field, lock_id=lock_id), "release")
        
        self.lock.pop(field)
        print(f"Released field {field} from ModifyCommit")
        return database.ModifyCommitResponse(success=True)

    def Lock(self, request, context):
        field = request.field
        if field in self.lock:
            if self.lock[field] > request.lock_id:
                return database.LockResponse(ok=False, other_id=self.lock[field])
            else:
                while field in self.lock:
                    if self.lock[field] > request.lock_id:
                        return database.LockResponse(ok=False, other_id=self.lock[field])
                    time.sleep(0.01)
        self.lock[field] = request.lock_id
        print(f"Locked field {field} with {request.lock_id} because of Lock")
        return database.LockResponse(ok=True, other_id=-1)

    def Release(self, request, context):
        if request.field in self.lock and self.lock[request.field] == request.lock_id:
            self.lock.pop(request.field)
            print(f"Released field {request.field} from Release")
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