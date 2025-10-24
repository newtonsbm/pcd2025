# entregas 
import pika
import json
import time
import random

HOST = 'rabbit'
nome = None
# random name
def gerar_nome():
    nomes = ['João', 'Maria', 'José', 'Pedro', 'Ana', 'Paulo', 'Luiz', 'Carlos']
    sobrenomes = ['Silva', 'Souza', 'Santos', 'Oliveira', 'Pereira', 'Lima', 'Ferreira']
    return f"{random.choice(nomes)} {random.choice(sobrenomes)}"

def rabbit_config():
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=HOST))
    channel = connection.channel()
    channel.queue_declare(queue='entregas')
    return channel

def realizar_entrega(channel, method, properties, body):
    global nome
    pedido = json.loads(body)
    print(f"Entregador(a) {nome} iniciando entrega do pedido {pedido['id']}") 
    tempo_entrega = pedido['tempo']
    time.sleep(tempo_entrega)
    print(f"Entregador(a) {nome} retornou") 
    

def main():
    global nome
    nome = gerar_nome()
    print(f"Entregador(a) pronto: {nome}...")
    channel = rabbit_config()
    channel.basic_consume(queue='entregas', on_message_callback=realizar_entrega)
    channel.start_consuming()


if __name__ == '__main__':
    main()