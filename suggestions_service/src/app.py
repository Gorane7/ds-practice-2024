import sys
import os
import random
import time

# This set of lines are needed to import the gRPC stubs.
# The path of the stubs is relative to the current file, or absolute inside the container.
# Change these lines only if strictly needed.
FILE = __file__ if '__file__' in globals() else os.getenv("PYTHONFILE", "")
utils_path = os.path.abspath(os.path.join(FILE, '../../../utils/pb/suggestions_service'))
sys.path.insert(0, utils_path)
import suggestions_service_pb2 as suggestions_service
import suggestions_service_pb2_grpc as suggestions_service_grpc

import grpc
from concurrent import futures

# Create a class to define the server functions, derived from
# suggestions_service_pb2_grpc.HelloServiceServicer
class SuggestionsService(suggestions_service_grpc.SuggestionsServiceServicer):
    # Create an RPC function to say hello
    def Suggest(self, request, context):
        start = time.time()
        response = suggestions_service.SuggestionResponse()
        if len(request.books) == 0:
            response = suggestions_service.SuggestionResponse(books = [])
        else:
            book = random.choice(request.books)
            response = suggestions_service.SuggestionResponse(books = [book])
        print(f"Pool of books to choose from: {[i.title for i in response.books]}")
        print(f"Book chosen to suggest: {book.title}")
        print(f"Time taken to choose book: {round(time.time()-start,4)}")
        return response

def serve():
    # Create a gRPC server
    server = grpc.server(futures.ThreadPoolExecutor())
    # Add HelloService
    suggestions_service_grpc.add_SuggestionsServiceServicer_to_server(SuggestionsService(), server)
    # Listen on port 50051
    port = "50053"
    server.add_insecure_port("[::]:" + port)
    # Start the server
    server.start()
    print("Server started. Listening on port 50053.")
    # Keep thread alive
    server.wait_for_termination()

if __name__ == '__main__':
    serve()