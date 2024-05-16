import sys
import os
import random
import time
from collections import defaultdict
import threading

import gensim.downloader as api

# This set of lines are needed to import the gRPC stubs.
# The path of the stubs is relative to the current file, or absolute inside the container.
# Change these lines only if strictly needed.
FILE = __file__ if '__file__' in globals() else os.getenv("PYTHONFILE", "")
utils_path = os.path.abspath(os.path.join(FILE, '../../../utils/pb/suggestions_service'))
sys.path.insert(0, utils_path)
import suggestions_service_pb2 as suggestions_service
import suggestions_service_pb2_grpc as suggestions_service_grpc

utils_path = os.path.abspath(os.path.join(FILE, '../../../utils/pb/fraud_detection'))
sys.path.insert(0, utils_path)

import fraud_detection_pb2 as fraud_detection
import fraud_detection_pb2_grpc as fraud_detection_grpc


import grpc
from concurrent import futures


from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry import metrics
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader

from opentelemetry.exporter.otlp.proto.http.metric_exporter import OTLPMetricExporter

resource = Resource(attributes={
    SERVICE_NAME: "suggestion_service"
})

metric_reader = PeriodicExportingMetricReader(OTLPMetricExporter("http://observability:4318/v1/metrics"))
provider = MeterProvider(metric_readers=[metric_reader], resource=resource)
metrics.set_meter_provider(provider)
meter = metrics.get_meter("suggestion.service.meter")
suggestion_counter = meter.create_counter("suggestion.counter", unit="1", description="Counts the number of suggestions that have been made")


suggestion_duration = meter.create_histogram(
    name="suggestion.duration",
    description="Measures the time it took to generate a suggestion",
    unit="ms")


word_vectors = api.load("word2vec-google-news-300")

def calculate_similarity(book, other_book):
    return word_vectors.n_similarity(book.lower().split(), other_book.lower().split())

# Create a class to define the server functions, derived from
# suggestions_service_pb2_grpc.HelloServiceServicer
class SuggestionsService(suggestions_service_grpc.SuggestionsServiceServicer):
    def __init__(self):
        self.vector_clock = defaultdict(lambda : [0,0,0])
        self.response = defaultdict(lambda : suggestions_service.SuggestionResponse())
        self.die = defaultdict(lambda : False)
        self.part1dep = [0,0,0]
        self.part2dep = [5,5,3]
    
    def VectorClockUpdate(self, request, context):
        self.vector_clock[request.order_id] = [max(self.vector_clock[request.order_id][i], request.vector_clock[i]) for i in range(len(request.vector_clock))]
        self.vector_clock[request.order_id][2] += 1
        print(f"Clock is {self.vector_clock[request.order_id]}")
        return suggestions_service.Empty_sugg()

    # Create an RPC function to say hello
    def Suggest(self, request, context):
        thread1 = threading.Thread(target=self.suggestPart1, args=(request.order_id, request))
        thread2 = threading.Thread(target=self.suggestPart2, args=(request.order_id, request))
        thread1.start()
        thread2.start()
        thread1.join()
        thread2.join()
        resp = self.response[request.order_id]
        if request.order_id in self.die:
            self.die.pop(request.order_id)
        if request.order_id in self.response:
            self.response.pop(request.order_id)
        if request.order_id in self.vector_clock:
            self.vector_clock.pop(request.order_id)
        return resp
    
    def suggestPart1(self, order_id, request):
        start = time.time()
        while self.die[order_id] or not self.depCheck(self.vector_clock[request.order_id], self.part1dep):
            time.sleep(0.1)
            if self.die[request.order_id]:
                return
        # Do something useful
        response = suggestions_service.SuggestionResponse()
        print(f"Time taken to verify book: {round(time.time()-start,4)}")
        self.response[order_id] = response
        self.vector_clock[order_id][2] += 2
        with grpc.insecure_channel('fraud_detection:50051') as channel:
            stub = fraud_detection_grpc.HelloServiceStub(channel)
            vec_clock_msg = fraud_detection.VectorClockInp_fraud()
            vec_clock_msg.vector_clock.extend(self.vector_clock[order_id])
            vec_clock_msg.order_id = order_id
            stub.VectorClockUpdate(vec_clock_msg)
    
    def suggestPart2(self, order_id, request):
        start = time.time()
        while self.die[order_id] or not self.depCheck(self.vector_clock[request.order_id], self.part2dep):
            time.sleep(0.1)
            if self.die[request.order_id]:
                return
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
                suggestion_counter.add(1)
                print(f"User ordered {ordered_book}, so suggesting {other_book}")
                if similarity < 0.01:
                    break
        response = suggestions_service.SuggestionResponse(books = suggested_books)

        if len(request.books) == 0:
            response = suggestions_service.SuggestionResponse(books = [])
        else:
            book = random.choice(request.books)
            response = suggestions_service.SuggestionResponse(books = [book])

        print(f"Books that were ordered by the user: {request.ordered}")
        print(f"Book chosen to suggest: {book.title}")
        time_taken = time.time() - start
        suggestion_duration.record(time_taken)
        print(f"Time taken to choose books: {round(time_taken, 4)}")
        
        self.response[order_id] = response
    
    def Kill(self, request, context):
        self.die[request.order_id] = True
        time.sleep(1)
        if request.order_id in self.vector_clock:
            self.vector_clock.pop(request.order_id)
        return  suggestions_service.Empty_sugg()

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