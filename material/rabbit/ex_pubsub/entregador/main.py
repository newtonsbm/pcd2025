#!/usr/bin/env python
"""
Serviço de Entrega
Recebe pedidos e organiza as entregas
"""
import pika
import json
import time
import random
import os

RABBIT_HOST = os.environ.get('RABBIT_HOST', 'localhost')
EXCHANGE_NAME = 'pedidos_pizzaria'

ENTREGADORES = ['🏍️ Moto 1', '🏍️ Moto 2', '🚗 Carro 1']

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
    
    # Cria fila exclusiva para este subscriber
    result = channel.queue_declare(queue='', exclusive=True)
    queue_name = result.method.queue
    
    channel.queue_bind(
        exchange=EXCHANGE_NAME,
        queue=queue_name
    )
    
    return connection, channel, queue_name

def calcular_tempo_entrega(endereco):
    """Calcula tempo estimado de entrega baseado no endereço."""
    # Simulação: endereços diferentes têm tempos diferentes
    return random.uniform(15, 45)  # 15 a 45 minutos

def callback(ch, method, properties, body):
    """Callback chamado quando um pedido é recebido."""
    pedido = json.loads(body.decode())
    
    print("\n" + "=" * 50)
    print(f"📦 NOVO PEDIDO PARA ENTREGA")
    print("=" * 50)
    print(f"   Pedido: #{pedido['numero_pedido']:03d}")
    print(f"   Cliente: {pedido['cliente']}")
    print(f"   Endereço: {pedido['endereco']}")
    print(f"   Itens: {pedido['quantidade']}x {pedido['pizza']}")
    
    # Designa um entregador aleatório
    entregador = random.choice(ENTREGADORES)
    tempo_estimado = calcular_tempo_entrega(pedido['endereco'])
    
    print(f"   🏍️ Entregador: {entregador}")
    print(f"   ⏱️ Tempo estimado: {tempo_estimado:.0f} minutos")
    print(f"   📍 Rota calculada para: {pedido['endereco']}")
    print("-" * 50)

def main():
    print("=" * 50)
    print("🏍️ ENTREGADORES - Serviço de Delivery")
    print("=" * 50)
    print()
    
    connection, channel, queue_name = conectar_rabbitmq()
    
    print(f"✓ Conectado ao RabbitMQ")
    print(f"✓ Inscrito no exchange '{EXCHANGE_NAME}'")
    print(f"✓ Fila: {queue_name}")
    print()
    print("🏍️ Entregadores prontos! Aguardando pedidos...")
    print("-" * 50)
    
    channel.basic_consume(
        queue=queue_name,
        on_message_callback=callback,
        auto_ack=True
    )
    
    try:
        channel.start_consuming()
    except KeyboardInterrupt:
        print("\n\n🛑 Serviço de entrega encerrado")
        channel.stop_consuming()
        connection.close()

if __name__ == '__main__':
    main()

