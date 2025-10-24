#!/usr/bin/env python
"""
Serviço da Cozinha
Recebe pedidos e simula o preparo das pizzas
"""
import pika
import json
import time
import random
import os

RABBIT_HOST = os.environ.get('RABBIT_HOST', 'localhost')
EXCHANGE_NAME = 'pedidos_pizzaria'

def conectar_rabbitmq():
    """Conecta ao RabbitMQ e configura subscriber."""
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=RABBIT_HOST)
    )
    channel = connection.channel()
    
    # Declara o exchange (pode ser declarado múltiplas vezes, é idempotente)
    channel.exchange_declare(
        exchange=EXCHANGE_NAME,
        exchange_type='fanout',
        durable=True
    )
    
    # Cria uma fila EXCLUSIVA e TEMPORÁRIA para este subscriber
    # exclusive=True: apenas esta conexão pode acessar
    # Quando a conexão fechar, a fila é automaticamente deletada
    result = channel.queue_declare(queue='', exclusive=True)
    queue_name = result.method.queue
    
    # Faz o BINDING: conecta a fila ao exchange
    # Agora todas as mensagens do exchange virão para esta fila
    channel.queue_bind(
        exchange=EXCHANGE_NAME,
        queue=queue_name
    )
    
    return connection, channel, queue_name

def preparar_pizza(pedido):
    """Simula o preparo de uma pizza."""
    tempo_preparo = random.uniform(2, 5)  # 2 a 5 segundos
    
    print(f"   👨‍🍳 Preparando {pedido['quantidade']}x {pedido['pizza']}...")
    time.sleep(tempo_preparo)
    print(f"   ✓ Pizza pronta! Tempo: {tempo_preparo:.1f}s")

def callback(ch, method, properties, body):
    """Callback chamado quando um pedido é recebido."""
    pedido = json.loads(body.decode())
    
    print("\n" + "=" * 50)
    print(f"🔔 NOVO PEDIDO RECEBIDO NA COZINHA")
    print("=" * 50)
    print(f"   Pedido: #{pedido['numero_pedido']:03d}")
    print(f"   Cliente: {pedido['cliente']}")
    print(f"   Item: {pedido['quantidade']}x {pedido['pizza']}")
    
    # Simula o preparo
    preparar_pizza(pedido)
    
    print(f"   🍕 Pedido #{pedido['numero_pedido']:03d} pronto para entrega!")
    print("-" * 50)

def main():
    print("=" * 50)
    print("👨‍🍳 COZINHA - Serviço de Preparo")
    print("=" * 50)
    print()
    
    connection, channel, queue_name = conectar_rabbitmq()
    
    print(f"✓ Conectado ao RabbitMQ")
    print(f"✓ Inscrito no exchange '{EXCHANGE_NAME}'")
    print(f"✓ Fila: {queue_name}")
    print()
    print("🔥 Forno aceso! Aguardando pedidos...")
    print("-" * 50)
    
    # Registra o callback
    channel.basic_consume(
        queue=queue_name,
        on_message_callback=callback,
        auto_ack=True
    )
    
    try:
        channel.start_consuming()
    except KeyboardInterrupt:
        print("\n\n🛑 Cozinha fechada")
        channel.stop_consuming()
        connection.close()

if __name__ == '__main__':
    main()

