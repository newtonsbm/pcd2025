#!/usr/bin/env python
"""
Serviço Financeiro
Registra vendas e calcula faturamento
"""
import pika
import json
import os

RABBIT_HOST = os.environ.get('RABBIT_HOST', 'localhost')
EXCHANGE_NAME = 'pedidos_pizzaria'

class ControladorFinanceiro:
    """Controla o faturamento da pizzaria."""
    
    def __init__(self):
        self.total_vendas = 0
        self.total_pedidos = 0
        self.faturamento = 0.0
    
    def registrar_venda(self, pedido):
        """Registra uma nova venda."""
        self.total_pedidos += 1
        self.total_vendas += pedido['quantidade']
        self.faturamento += pedido['preco_total']
    
    def exibir_resumo(self, pedido):
        """Exibe resumo financeiro."""
        print(f"\n   💰 RESUMO FINANCEIRO")
        print(f"   ├─ Valor desta venda: R$ {pedido['preco_total']:.2f}")
        print(f"   ├─ Total de pedidos: {self.total_pedidos}")
        print(f"   ├─ Total de pizzas: {self.total_vendas}")
        print(f"   └─ Faturamento acumulado: R$ {self.faturamento:.2f}")

controlador = ControladorFinanceiro()

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

def callback(ch, method, properties, body):
    """Callback chamado quando um pedido é recebido."""
    pedido = json.loads(body.decode())
    
    print("\n" + "=" * 50)
    print(f"💵 NOVA VENDA REGISTRADA")
    print("=" * 50)
    print(f"   Pedido: #{pedido['numero_pedido']:03d}")
    print(f"   Item: {pedido['quantidade']}x {pedido['pizza']}")
    print(f"   Valor: R$ {pedido['preco_total']:.2f}")
    
    # Registra a venda
    controlador.registrar_venda(pedido)
    
    # Exibe resumo
    controlador.exibir_resumo(pedido)
    
    print("-" * 50)

def main():
    print("=" * 50)
    print("💰 FINANCEIRO - Controle de Vendas")
    print("=" * 50)
    print()
    
    connection, channel, queue_name = conectar_rabbitmq()
    
    print(f"✓ Conectado ao RabbitMQ")
    print(f"✓ Inscrito no exchange '{EXCHANGE_NAME}'")
    print(f"✓ Fila: {queue_name}")
    print()
    print("💰 Sistema financeiro ativo!")
    print("-" * 50)
    
    channel.basic_consume(
        queue=queue_name,
        on_message_callback=callback,
        auto_ack=True
    )
    
    try:
        channel.start_consuming()
    except KeyboardInterrupt:
        print("\n\n" + "=" * 50)
        print("📊 RELATÓRIO FINAL")
        print("=" * 50)
        print(f"Total de pedidos: {controlador.total_pedidos}")
        print(f"Total de pizzas: {controlador.total_vendas}")
        print(f"Faturamento total: R$ {controlador.faturamento:.2f}")
        print("=" * 50)
        print("\n🛑 Serviço financeiro encerrado")
        channel.stop_consuming()
        connection.close()

if __name__ == '__main__':
    main()

