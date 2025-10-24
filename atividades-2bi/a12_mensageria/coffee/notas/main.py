# sistema cafe com pao
import pika
import json

HOST = 'rabbit'
total_pedidos = 0
total_valor = 0

def rabbit_config():
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=HOST))
    channel = connection.channel()
    channel.queue_declare(queue='notas') 
    return channel

def processar_pedido(channel, method, properties, body):
    global total_valor
    global total_pedidos
    pedido = json.loads(body)
    total_pedidos += 1
    total_valor += pedido['valor']
    print(f"Nota gerada para pedido {pedido['id']}")
    print(f"- Total de pedidos: {total_pedidos}")
    print(f"- Total de valores processados: R${total_valor}")

def main():
    print("Iniciando sistema de notas...")
    channel = rabbit_config()
    channel.basic_consume(queue='notas', on_message_callback=processar_pedido, auto_ack=True)
    channel.start_consuming()


if __name__ == '__main__':
    main()