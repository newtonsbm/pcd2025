# WHATSAPP 
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
    channel.queue_declare(queue='whatsapp', exclusive=True)
    channel.queue_bind(exchange='notificacoes', queue='whatsapp')
    return channel

def enviar_whatsapp(channel, method, properties, body):
    tempo_envio = random.randint(0, 3)
    time.sleep(tempo_envio)
    pedido = json.loads(body)
    print(f"WhatsApp enviado - pedido {pedido['id']}")

def main():
    print("Iniciando integração com Whatsapp...")
    channel = rabbit_config()
    channel.basic_consume(queue='whatsapp', on_message_callback=enviar_whatsapp, auto_ack=True)
    channel.start_consuming()


if __name__ == '__main__':
    main()