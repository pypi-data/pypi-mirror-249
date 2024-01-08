import pika, os, time

RABBITMQ_DEFAULT_HOST = os.environ.get('RABBITMQ_DEFAULT_HOST')
RABBITMQ_DEFAULT_PORT = os.environ.get('RABBITMQ_DEFAULT_PORT')

RABBITMQ_DEFAULT_USER = os.environ.get('RABBITMQ_DEFAULT_USER')
RABBITMQ_DEFAULT_PASS = os.environ.get('RABBITMQ_DEFAULT_PASS')

def create_connection(**kwargs):
  host = kwargs['host'] if 'host' in kwargs else RABBITMQ_DEFAULT_HOST
  port = kwargs['port'] if 'port' in kwargs else RABBITMQ_DEFAULT_PORT
  user = kwargs['username'] if 'username' in kwargs else RABBITMQ_DEFAULT_USER
  passwd = kwargs['password'] if 'password' in kwargs else RABBITMQ_DEFAULT_PASS
  
  while True:
    try:
      credentials = pika.PlainCredentials(user, passwd)
      connection = pika.BlockingConnection(pika.ConnectionParameters(host, port, '/', credentials))
      print("Connected to RabbitMQ successfully.")
      return connection.channel(), connection 
    except pika.exceptions.AMQPConnectionError as e:
      print("Failed to connect to RabbitMQ. Retrying in 5 seconds...")
      print(e)
      time.sleep(5)
  
