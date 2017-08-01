import pika, uuid

class AuthClient(object):
    def __init__ (self, host="localhost", port=5672):
        self.connection = pika.BlockingConnection(
            host = host,
            port = port
        )
        self.channel = self.connection.channel()
        result = self.channel_queue_declare(exclusive=True)
        self.callback_queue = result.method.queue
        self.channel.basic_consume(
            self.on_response,
            no_ack=True,
            queue=self.callback_queue
        )

    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = body

    def isValidToken_Remote(self, token):
        self.response = None
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(
            exchange="",
            routing_key='rpc_validToken',
            properties=pika.BasicProperties(
                reply_to = self.callback_queue,
                correlation_id = self.corr_id,
            ),
            body = token
        )
        while self.response is None:
            self.connection.process_data_events()
        return bool(self.response)

authClient = AuthClient(host="192.168.99.100")
print(authClient.isValidToken_Remote("355325353gs3532"))
