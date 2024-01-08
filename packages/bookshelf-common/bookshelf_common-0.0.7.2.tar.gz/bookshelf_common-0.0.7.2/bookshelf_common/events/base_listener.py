from bookshelf_common.events import create_connection, QueueList
from typing import List
from datetime import datetime

TIME_FORMAT = "%Y-%m-%d %H:%M:%S"

def init_listener(exchange_subject, queue_subject, callback, exchange_type='fanout', channel=None, **kwargs):
  now = datetime.now()
  if channel is None:
    channel, connection = create_connection(**kwargs)
  # Create fanout exchange
  channel.exchange_declare(exchange=exchange_subject, exchange_type=exchange_type)
  
  # Create queues and bind them to the exchange
  queue = channel.queue_declare(queue=queue_subject)
  channel.queue_bind(exchange=exchange_subject, queue=queue.method.queue)

  # Set up consumers
  channel.basic_consume(queue=queue.method.queue, on_message_callback=callback)
  
  print(f'{now.strftime(TIME_FORMAT)} [*] Waiting for messages. To exit press CTRL+C')
  
  # Start consuming
  channel.start_consuming()

def init_multiple_listeners(queue_list: List[QueueList], exchange_type='fanout', **kwargs):
  now = datetime.now()
  if channel is None:
    channel, connection = create_connection(**kwargs)

  for x in queue_list:
    # Create fanout exchange
    channel.exchange_declare(exchange=x.exchange_subject, exchange_type=exchange_type)
    
    # Create queues and bind them to the exchange
    queue = channel.queue_declare(queue=x.queue_subject)
    channel.queue_bind(exchange=x.exchange_subject, queue=queue.method.queue)

    # Set up consumers
    channel.basic_consume(queue=queue.method.queue, on_message_callback=x.callback)

  print(f'{now.strftime(TIME_FORMAT)} [*] Waiting for messages. To exit press CTRL+C')

  # Start consuming
  channel.start_consuming()
