
import os
import pika # type: ignore
import json
from dotenv import load_dotenv # type: ignore

# Load environment variables from .env file
load_dotenv()
AMQP_URL = os.getenv("AMQP_URL")

# Establish connection and channel
connection = pika.BlockingConnection(pika.URLParameters(AMQP_URL))
channel = connection.channel()

# Declare queue (creates if not exists)
channel.queue_declare(queue='demo_queue', durable=True)

# Message to send
message = {
    "query": "What is RAG?",
    "user_id": 123
}

# Send message to queue
channel.basic_publish(
    exchange='',
    routing_key='demo_queue',
    body=json.dumps(message),
    properties=pika.BasicProperties(delivery_mode=2)  # make message persistent
)

print("📤 Sent message:", message)

# Close connection
connection.close()
