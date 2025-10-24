# sistema cafe com pao
from datetime import datetime
import random
import time
import pika
import json

HOST = 'rabbit'

def rabbit_config():
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=HOST))
    channel = connection.channel()
    channel.exchange_declare(exchange='notificacoes', exchange_type='fanout')
    channel.queue_declare(queue='notas') 
    channel.queue_declare(queue='entregas') 
    return channel

def gerar_pedido(id):
    novo_pedido = {
        'id': id,
        'tempo': random.randint(2, 20),
        'valor': random.randint(20, 200),
        'data': datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
    }
    print(f"Novo pedido gerado: {novo_pedido['id']}")
    return novo_pedido

def notificar_pedido(channel, pedido):
    # fanout - publish / subscribe
    channel.basic_publish(exchange='notificacoes', routing_key='', body=json.dumps(pedido))

def entregar_pedido(channel, pedido):
    # direct - pipeline
    channel.basic_publish(exchange='', routing_key='entregas', body=json.dumps(pedido))

def gerar_nota(channel, pedido):
    # direct only
    channel.basic_publish(exchange='', routing_key='notas', body=json.dumps(pedido))

def main():
    print("Iniciando sistema café com pão...")
    channel = rabbit_config()
    id = 1
    while True:
        novo_pedido = gerar_pedido(id)
        notificar_pedido(channel, novo_pedido)
        entregar_pedido(channel, novo_pedido)
        gerar_nota(channel, novo_pedido)
        time.sleep(3)
        id += 1

if __name__ == '__main__':
    main()