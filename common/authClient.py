import pika
import threading
from time import sleep 
import json

class AuthClient(object):
    internal_lock = threading.Lock()
    tokens = {}
    def __init__ (self, host="localhost"):
        self.connection= pika.BlockingConnection(
            pika.ConnectionParameters(host=host)
        )
        self.channel = self.connection.channel()
        self.channel.exchange_declare(exchange='auth', type='fanout')
        result = self.channel.queue_declare(exclusive=True)
        self.queue_name = result.method.queue
        self.channel.queue_bind(exchange = 'auth', queue = self.queue_name)
        thread = threading.Thread(target=self._process_data_events)
        thread.setDaemon(True)
        thread.start()

    def _process_data_events(self):
        self.channel.basic_consume(self._on_response, no_ack=True, queue=self.queue_name)
        while True:
            with self.internal_lock:
                self.connection.process_data_events()
                sleep(0.1)

    def _on_response(self, ch, method, props, body):
        data = json.loads(body)
        if data is not None:
            self.tokens[data["token"]] = data["id"]
        print(self.tokens)

    def isTokenValid(self, token, userID):
        if not token in self.tokens:
            return False
        return int(self.tokens[token]) == int(userID)

    def close():
        self.connection.close()

authClient = AuthClient(host="192.168.99.100")
while True:
    sleep(0.1)
