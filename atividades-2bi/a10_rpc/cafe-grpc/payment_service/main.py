import os
import time
import random
import grpc
import notification_pb2
import notification_pb2_grpc


NOTIFICATION_SERVICE_HOST = os.environ.get("NOTIFICATION_SERVICE_HOST")
NOTIFICATION_SERVICE_PORT = os.environ.get("NOTIFICATION_SERVICE_PORT")

class PaymentService:

    def __init__(self, notification_service_host, notification_service_port):
        channel = grpc.insecure_channel(f"{notification_service_host}:{notification_service_port}")
        self.notification_service_stub = notification_pb2_grpc.NotificationServiceStub(channel)

    def processar_pagamento(self, client, product, cost):
        print("\n" + "="*60)
        print("PAYMENT SERVICE - Processando novo pagamento...")
        print("="*60)
        
        # Simula processamento de pagamento com status aleatório
        statuses = ["sucesso", "negado", "pendente", "cancelado"]
        payment_status = random.choice(statuses)
        
        print(f"Cliente: {client}")
        print(f"Produto: {product}")
        print(f"Valor: R$ {cost:.2f}")
        print(f"Status do Pagamento: {payment_status.upper()}")
        print("-"*60)
        
        # Chamada gRPC para o Notification Service
        print("📡 Iniciando chamada gRPC para o Notification Service...")
        print(f"   └─> Enviando: NotificarPagamento(client={client}, product={product})")
        
        try:
            self.notification_service_stub.NotificarPagamento(
                notification_pb2.PaymentRequest(
                    client=client, 
                    product=product, 
                    payment_status=payment_status, 
                    cost=cost
                )
            )
            print("Chamada gRPC concluída com sucesso!")
        except grpc.RpcError as e:
            print(f"Erro na chamada gRPC: {e.code()}")
            print(f"   Detalhes: {e.details()}")
        
        print("="*60)

if __name__ == "__main__":
    print("\n" + "-"*30)
    print("PAYMENT SERVICE - Iniciando aplicação...")
    print("-"*30)
    print("\n️  Configurações:")
    print(f"   • Host do Notification Service: {NOTIFICATION_SERVICE_HOST}")
    print(f"   • Porta do Notification Service: {NOTIFICATION_SERVICE_PORT}")
    print("   • Intervalo entre transações: 3 segundos")
    
    # Inicializa o serviço de pagamento
    print(f"\nConectando ao Notification Service em {NOTIFICATION_SERVICE_HOST}:{NOTIFICATION_SERVICE_PORT}...")
    payment_service = PaymentService(NOTIFICATION_SERVICE_HOST, NOTIFICATION_SERVICE_PORT)
    print("Conexão estabelecida!\n")
    
    # Dados de exemplo para simulação
    clients = ["Mariana", "João", "Maria"]
    products = ["Café", "Pão", "Leite"]
    costs = [4.99, 2.49, 1.99]
    
    print("Iniciando simulação de transações...")
    print("   (Pressione Ctrl+C para interromper)\n")
    
    transaction_count = 0
    
    try:
        while True:
            transaction_count += 1
            print(f"\nTransação #{transaction_count}")
            
            # Seleciona dados aleatórios
            client = random.choice(clients)
            product = random.choice(products)
            cost = random.choice(costs)
            
            # Processa o pagamento
            payment_service.processar_pagamento(client, product, cost)
            
            # Aguarda antes da próxima transação
            print("\nAguardando 3 segundos até a próxima transação...")
            time.sleep(3)
    except KeyboardInterrupt:
        print("\n\nAplicação interrompida pelo usuário.")
        print(f"Total de transações processadas: {transaction_count}")
        print("Encerrando Payment Service...\n")
