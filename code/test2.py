import os
import pika # type: ignore
import json
from dotenv import load_dotenv # type: ignore

# Load environment variables from .env file
load_dotenv()
AMQP_URL = os.getenv("AMQP_URL")

# Callback to process message
def callback(ch, method, properties, body):
    message = json.loads(body)
    print("📥 Received message:", message)

# Connect to RabbitMQ
connection = pika.BlockingConnection(pika.URLParameters(AMQP_URL))
channel = connection.channel()

# Declare the same queue
channel.queue_declare(queue='demo_queue', durable=True)

# Start consuming messages
channel.basic_consume(
    queue='demo_queue',
    on_message_callback=callback,
    auto_ack=True
)

print("🔁 Waiting for messages... Press CTRL+C to stop.")
channel.start_consuming()
