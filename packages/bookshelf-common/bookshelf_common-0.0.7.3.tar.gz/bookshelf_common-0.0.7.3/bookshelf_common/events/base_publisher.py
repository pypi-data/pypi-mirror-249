from bookshelf_common.events import create_connection

def publish_message(obj, exchange_type='fanout', channel=None, connection=None, **kwargs):
  if channel is None:
    channel, connection = create_connection(**kwargs)
  
  message_body = obj.message_body

  # Create fanout exchange
  channel.exchange_declare(exchange=obj.subject, exchange_type=exchange_type)

  # Publish the message to the fanout exchange
  channel.basic_publish(exchange=obj.subject, routing_key='', body=message_body)
  
  print(f" [x] Sent user creation message: {message_body}")
  # Close the connection
  connection.close()
