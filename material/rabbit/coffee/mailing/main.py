# mailing
import pika
import json
import time
import random

HOST = 'rabbit'

def rabbit_config():
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=HOST))
    channel = connection.channel()
    channel.exchange_declare(exchange='notificacoes', exchange_type='fanout')
    channel.queue_declare(queue='mailing', exclusive=True)
    channel.queue_bind(exchange='notificacoes', queue='mailing')
    return channel

def enviar_email(channel, method, properties, body):
    tempo_envio = random.randint(1, 5)
    time.sleep(tempo_envio)
    pedido = json.loads(body)
    print(f"Enviando email para pedido {pedido['id']}")

def main():
    print("Iniciando serviço de mailing...")
    channel = rabbit_config()
    channel.basic_consume(queue='mailing', on_message_callback=enviar_email, auto_ack=True)
    channel.start_consuming()


if __name__ == '__main__':
    main()