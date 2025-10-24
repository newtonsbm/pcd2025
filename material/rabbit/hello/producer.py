import pika

# Conectando com o rabbit 
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# Criando 1 fila
channel.queue_declare(queue='hello')

# Enviando 1 msg para fila

channel.basic_publish(exchange='',
                      routing_key='hello', # nome da fila
                      body='Hello World!')
print(" [x] Sent 'Hello World!'")

connection.close()


