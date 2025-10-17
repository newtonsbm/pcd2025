import time
import grpc
from concurrent import futures
import notification_pb2
import notification_pb2_grpc

class NotificationService(notification_pb2_grpc.NotificationServiceServicer):
    def __init__(self):
        super().__init__()
        self.notification_count = 0
    
    def NotificarPagamento(self, request, context):
        self.notification_count += 1
        
        # Extrai dados da requisição
        client = request.client
        product = request.product
        payment_status = request.payment_status
        cost = request.cost
        
        print("\n" + "="*60)
        print("NOTIFICATION SERVICE - Nova requisição recebida")
        print("="*60)
        print(f"Notificação #{self.notification_count}")
        print("Método RPC: NotificarPagamento")
        print("-"*60)
        print("Dados recebidos:")
        print(f"   Cliente: {client}")
        print(f"   Produto: {product}")
        print(f"   Status: {payment_status.upper()}")
        print(f"   Custo: R$ {cost:.2f}")
        print("-"*60)
        
        # Simula processamento da notificação
        print("Processando notificação...")
        print("   > Enviando SMS...")
        time.sleep(0.7)
        print("   > Enviando Email...")
        time.sleep(0.7)
        print("   > Enviando Push Notification...")
        time.sleep(0.6)
        
        print("Todas as notificações foram enviadas com sucesso!")
        print("="*60)
        
        return notification_pb2.PaymentResponse(
            message=f"Notificações enviadas para {client} sobre {product}"
        )

def serve():
    print("\n" + "="*60)
    print("NOTIFICATION SERVICE - Servidor gRPC")
    print("="*60)
    print("\nConfigurações do Servidor:")
    print("   • Protocolo: gRPC (insecure)")
    print("   • Porta: 8081")
    print("   • Workers: 10 threads")
    print("   • Interface: [::]  (todas as interfaces)")
    
    # Cria o servidor gRPC
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    
    # Registra o serviço
    notification_service = NotificationService()
    notification_pb2_grpc.add_NotificationServiceServicer_to_server(
        notification_service, 
        server
    )
    
    # Define a porta
    server.add_insecure_port('[::]:8081')
    
    print("\nIniciando servidor gRPC...")
    server.start()
    print("Servidor iniciado com sucesso!")
    print("Aguardando requisições na porta 8081...")
    print("(Pressione Ctrl+C para interromper)\n")
    
    try:
        server.wait_for_termination()
    except KeyboardInterrupt:
        print("\n\nServidor interrompido pelo usuário.")
        print(f"Total de notificações processadas: {notification_service.notification_count}")
        print("Encerrando servidor gRPC...")
        server.stop(grace=5)
        print("Notification Service encerrado.\n")

if __name__ == "__main__":
    serve()