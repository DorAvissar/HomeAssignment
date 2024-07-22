import pika

def publish_messages():
    # Connect to RabbitMQ server
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    # Declare a queue named 'ABC'
    channel.queue_declare(queue='ABC')

    # Publish messages to the queue
    for i in range(10):
        message = f"Message {i+1}"
        channel.basic_publish(exchange='',
                              routing_key='ABC',
                              body=message)
        print(f" [x] Sent '{message}'")

    # Close the connection
    connection.close()

if __name__ == "__main__":
    publish_messages()
