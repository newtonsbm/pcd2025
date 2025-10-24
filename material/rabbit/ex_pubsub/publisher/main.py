#!/usr/bin/env python
"""
Sistema de Pedidos da Pizzaria Digital
Publica pedidos para todos os serviços interessados
"""
import pika
import json
import time
import random
import os
from datetime import datetime

RABBIT_HOST = os.environ.get('RABBIT_HOST', 'localhost')
EXCHANGE_NAME = 'pedidos_pizzaria'

# Dados para gerar pedidos aleatórios
PIZZAS = [
    {'nome': 'Margherita', 'preco': 35.00},
    {'nome': 'Calabresa', 'preco': 38.00},
    {'nome': 'Portuguesa', 'preco': 42.00},
    {'nome': 'Quatro Queijos', 'preco': 45.00},
    {'nome': 'Pepperoni', 'preco': 48.00},
    {'nome': 'Frango com Catupiry', 'preco': 40.00},
    {'nome': 'Vegetariana', 'preco': 38.00},
    {'nome': 'Bacon', 'preco': 44.00},
]

CLIENTES = [
    'João Silva',
    'Maria Santos',
    'Pedro Oliveira',
    'Ana Costa',
    'Carlos Souza',
    'Juliana Lima',
    'Fernando Alves',
    'Patrícia Rocha',
]

ENDERECOS = [
    'Rua das Flores, 123',
    'Av. Principal, 456',
    'Rua do Comércio, 789',
    'Praça Central, 101',
    'Rua da Paz, 202',
    'Av. Brasil, 303',
]

def conectar_rabbitmq():
    """Conecta ao RabbitMQ e configura o exchange."""
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=RABBIT_HOST)
    )
    channel = connection.channel()
    
    # Declara um exchange do tipo FANOUT
    # fanout = envia para TODAS as filas conectadas (broadcast)
    channel.exchange_declare(
        exchange=EXCHANGE_NAME,
        exchange_type='fanout',
        durable=True  # Exchange sobrevive a reinicialização do RabbitMQ
    )
    
    return connection, channel

def gerar_pedido(numero_pedido):
    """Gera um pedido aleatório de pizza."""
    pizza = random.choice(PIZZAS)
    cliente = random.choice(CLIENTES)
    endereco = random.choice(ENDERECOS)
    quantidade = random.randint(1, 3)
    
    pedido = {
        'numero_pedido': numero_pedido,
        'cliente': cliente,
        'pizza': pizza['nome'],
        'quantidade': quantidade,
        'preco_unitario': pizza['preco'],
        'preco_total': pizza['preco'] * quantidade,
        'endereco': endereco,
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'status': 'novo'
    }
    
    return pedido

def publicar_pedido(channel, pedido):
    """Publica um pedido no exchange."""
    mensagem = json.dumps(pedido, ensure_ascii=False)
    
    # Publica no exchange (não em uma fila específica!)
    # routing_key vazio porque fanout ignora routing keys
    channel.basic_publish(
        exchange=EXCHANGE_NAME,
        routing_key='',  # Ignorado em fanout
        body=mensagem,
        properties=pika.BasicProperties(
            delivery_mode=2,  # Mensagem persistente
            content_type='application/json'
        )
    )

def main():
    print("=" * 60)
    print("🍕 PIZZARIA DIGITAL - Sistema de Pedidos")
    print("=" * 60)
    print()
    
    connection, channel = conectar_rabbitmq()
    print(f"✓ Conectado ao RabbitMQ")
    print(f"✓ Exchange '{EXCHANGE_NAME}' (tipo: fanout) configurado")
    print()
    print("📢 Publicando pedidos para TODOS os serviços...")
    print("   (Cozinha, Entregadores, App, Financeiro, etc.)")
    print()
    print("-" * 60)
    
    numero_pedido = 1
    
    try:
        while True:
            # Gera um novo pedido
            pedido = gerar_pedido(numero_pedido)
            
            # Publica o pedido
            publicar_pedido(channel, pedido)
            
            # Exibe informações do pedido
            print(f"\n🍕 PEDIDO #{pedido['numero_pedido']:03d} PUBLICADO")
            print(f"   Cliente: {pedido['cliente']}")
            print(f"   Pizza: {pedido['quantidade']}x {pedido['pizza']}")
            print(f"   Total: R$ {pedido['preco_total']:.2f}")
            print(f"   Endereço: {pedido['endereco']}")
            print(f"   Horário: {pedido['timestamp']}")
            print("-" * 60)
            
            numero_pedido += 1
            
            # Aguarda entre 3 e 8 segundos antes do próximo pedido
            time.sleep(random.uniform(3, 8))
            
    except KeyboardInterrupt:
        print("\n\n🛑 Sistema de pedidos encerrado")
        connection.close()

if __name__ == '__main__':
    main()

