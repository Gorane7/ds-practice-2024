import sys
import os
import random
import time

import gensim.downloader as api

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


word_vectors = api.load("word2vec-google-news-300")

def calculate_similarity(book, other_book):
    return word_vectors.n_similarity(book.lower().split(), other_book.lower().split())

# Create a class to define the server functions, derived from
# suggestions_service_pb2_grpc.HelloServiceServicer
class SuggestionsService(suggestions_service_grpc.SuggestionsServiceServicer):
    def __init__(self):
        self.vector_clock = [0,0,0,0,0]
    
    def VectorClockUpdate(self, request, context):
        self.vector_clock = [max(self.vector_clock[i], request.vector_clock[i]) for i in range(3)]
        return suggestions_service.Empty_sugg()

    # Create an RPC function to say hello
    def Suggest(self, request, context):
        start = time.time()
        while not self.depCheck(self.vector_clock, [1,1,1,1,0]):
            time.sleep(0.1)
        suggested_books = []
        book_pool = [i.title for i in request.books]
        print(f"Pool of books to choose from: {book_pool}")
        for ordered_book in request.ordered:
            similarities = [(other_book, calculate_similarity(ordered_book, other_book)) for other_book in book_pool]
            sorted_books = sorted(similarities, key=lambda x: x[1], reverse=True)
            for other_book, similarity in sorted_books:
                if other_book == ordered_book:
                    continue
                suggested_books.append(request.books[book_pool.index(other_book)])
                print(f"User ordered {ordered_book}, so suggesting {other_book}")
                break
        response = suggestions_service.SuggestionResponse(books = suggested_books)

        if len(request.books) == 0:
            response = suggestions_service.SuggestionResponse(books = [])
        else:
            book = random.choice(request.books)
            response = suggestions_service.SuggestionResponse(books = [book])

        print(f"Books that were ordered by the user: {request.ordered}")
        print(f"Book chosen to suggest: {book.title}")
        print(f"Time taken to choose books: {round(time.time()-start,4)}")
        return response
    
    def depCheck(self, vec1, vec2):
        return min([vec1[i]>=vec2[i] for i in range(len(vec1))])

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