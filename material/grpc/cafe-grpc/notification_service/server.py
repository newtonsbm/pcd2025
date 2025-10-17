import time
import grpc
from concurrent import futures
import notification_pb2
import notification_pb2_grpc

class NotificationService(notification_pb2_grpc.NotificationServiceServicer):
    def NotificarPagamento(self, request, context):
        client = request.client
        product = request.product
        payment_status = request.payment_status
        cost = request.cost

        print(f"Notificando client #{client} sobre o pagamento da {product}:")
        print(f"Status: {payment_status}, Custo: ${cost}")
        time.sleep(2)
        print("Notificações enviadas!")

        return notification_pb2.PaymentResponse(message="Notificações enviadas!")

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    notification_pb2_grpc.add_NotificationServiceServicer_to_server(NotificationService(), server)
    server.add_insecure_port('[::]:8081')
    print("Iniciando serviço de notificação...")
    server.start()
    server.wait_for_termination()

if __name__ == "__main__":
    serve()