#!/usr/bin/env python
"""
Serviço de Notificações (App)
Envia notificações push/SMS para clientes
"""
import pika
import json
import os

RABBIT_HOST = os.environ.get('RABBIT_HOST', 'localhost')
EXCHANGE_NAME = 'pedidos_pizzaria'

def conectar_rabbitmq():
    """Conecta ao RabbitMQ e configura subscriber."""
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=RABBIT_HOST)
    )
    channel = connection.channel()
    
    channel.exchange_declare(
        exchange=EXCHANGE_NAME,
        exchange_type='fanout',
        durable=True
    )
    
    result = channel.queue_declare(queue='', exclusive=True)
    queue_name = result.method.queue
    
    channel.queue_bind(
        exchange=EXCHANGE_NAME,
        queue=queue_name
    )
    
    return connection, channel, queue_name

def enviar_sms(pedido):
    """Simula envio de SMS."""
    mensagem = (
        f"🍕 Olá {pedido['cliente']}! "
        f"Seu pedido #{pedido['numero_pedido']:03d} foi confirmado! "
        f"{pedido['quantidade']}x {pedido['pizza']}. "
        f"Total: R$ {pedido['preco_total']:.2f}"
    )
    print(f"   📱 SMS: {mensagem}")

def enviar_push(pedido):
    """Simula envio de notificação push."""
    print(f"   🔔 PUSH: Pedido #{pedido['numero_pedido']:03d} confirmado!")

def enviar_email(pedido):
    """Simula envio de email."""
    print(f"   📧 EMAIL para {pedido['cliente']}")
    print(f"      Assunto: Pedido #{pedido['numero_pedido']:03d} Confirmado")

def callback(ch, method, properties, body):
    """Callback chamado quando um pedido é recebido."""
    pedido = json.loads(body.decode())
    
    print("\n" + "=" * 50)
    print(f"📱 ENVIANDO NOTIFICAÇÕES")
    print("=" * 50)
    print(f"   Pedido: #{pedido['numero_pedido']:03d}")
    print(f"   Cliente: {pedido['cliente']}")
    print()
    
    # Envia múltiplas notificações
    enviar_push(pedido)
    enviar_sms(pedido)
    enviar_email(pedido)
    
    print(f"\n   ✓ Todas as notificações enviadas!")
    print("-" * 50)

def main():
    print("=" * 50)
    print("📱 APP - Serviço de Notificações")
    print("=" * 50)
    print()
    
    connection, channel, queue_name = conectar_rabbitmq()
    
    print(f"✓ Conectado ao RabbitMQ")
    print(f"✓ Inscrito no exchange '{EXCHANGE_NAME}'")
    print(f"✓ Fila: {queue_name}")
    print()
    print("📱 Sistema de notificações ativo!")
    print("-" * 50)
    
    channel.basic_consume(
        queue=queue_name,
        on_message_callback=callback,
        auto_ack=True
    )
    
    try:
        channel.start_consuming()
    except KeyboardInterrupt:
        print("\n\n🛑 Serviço de notificações encerrado")
        channel.stop_consuming()
        connection.close()

if __name__ == '__main__':
    main()

