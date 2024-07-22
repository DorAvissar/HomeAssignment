# Step 4: Documentation

Setup RabbitMQ Using Docker:

```
docker run -d --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:3-management
```

Install Python Dependencies:
In this task we're going to use Pika 1.0.0, which is the Python client recommended by the RabbitMQ team. To install it you can use the pip package management tool:
```
pip install pika
```
## Sending
Our first program send.py will send messages to the queue. The first thing we need to do is to establish a connection with RabbitMQ server.
```
import pika

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
```
We're connected now, to a broker on the local machine - hence the localhost. If we wanted to connect to a broker on a different machine we'd simply specify its name or IP address here.

Next, before sending we need to make sure the recipient queue exists. If we send a message to non-existing location, RabbitMQ will just drop the message. 
```
channel.queue_declare(queue='ABC')
```
Next - The loop iterates 10 times.

In each iteration, it creates a message string labeled "Message 1", "Message 2", ..., "Message 10".

It sends each message to the RabbitMQ queue named 'ABC'.

It prints a confirmation message to the console for each message sent.:
```
for i in range(10):
        message = f"Message {i+1}"
        channel.basic_publish(exchange='',
                              routing_key='ABC',
                              body=message)
        print(f" [x] Sent '{message}'")

```

Before exiting the program we need to make sure the network buffers were flushed and our message was actually delivered to RabbitMQ. We can do it by gently closing the connection.
```
connection.close()
```

## Receiving

Our second program receive.py will receive messages from the queue and print them on the screen.

Again, first we need to connect to RabbitMQ server. The code responsible for connecting to Rabbit is the same as previously.

The next step, just like before, is to make sure that the queue exists. Creating a queue using queue_declare is idempotent ‒ we can run the command as many times as we like, and only one will be created.
```
channel.queue_declare(queue='ABC')
```
Receiving messages from the queue is more complex. It works by subscribing a callback function to a queue. Whenever we receive a message, this callback function is called by the Pika library. In our case this function will print on the screen the contents of the message.
```
def callback(ch, method, properties, body):
    print(f" [x] Received {body}")
```
Next, we need to tell RabbitMQ that this particular callback function should receive messages from our hello queue:
```
channel.basic_consume(queue='ABC',
                      auto_ack=True,
                      on_message_callback=callback)
```
And finally, we enter a never-ending loop that waits for data and runs callbacks whenever necessary, and catch KeyboardInterrupt during program shutdown.
```
print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
```
```
if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)

```

Now we can try out our programs in a terminal. 
First,
Setup RabbitMQ Using Docker:

```
docker run -d --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:3-management
```

Second - start a consumer, which will run continuously waiting for deliveries:

Run the Consumer:
```
python receive.py
``` 

Run the Publisher:
```
python send.py
```



