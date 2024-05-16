import sys
import os
import threading
import time
import random
import grpc

FILE = __file__ if '__file__' in globals() else os.getenv("PYTHONFILE", "")

utils_path = os.path.abspath(os.path.join(FILE, '../../utils/pb/database'))
sys.path.insert(0, utils_path)

import database_pb2 as database
import database_pb2_grpc as database_grpc


with grpc.insecure_channel('localhost:50105') as channel:
    db = {f"book_{i}": 10 for i in range(100)}
    db["Learning Python"] = 10
    db_aslist = []
    for k in db:
        db_aslist.append({"book_name": k, "amount": db[k]})
    
    stub = database_grpc.DatabaseStub(channel)
    stub.OverwriteDB(database.OverwriteDBRequest(fields=db_aslist))

