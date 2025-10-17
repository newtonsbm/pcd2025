import rpyc
import time

PORT = 18861

class NotificationService(rpyc.Service):

    def on_connect(self, conn):
        print("Servico conectado")

    def on_disconnect(self, conn):
        print("Servico desconectado")

    def exposed_notificar_pagamento(self, client, product, payment_status, cost):
        print(f"Notificando client #{client} sobre o pagamento da {product}:")
        print(f"Status: {payment_status}, Custo: ${cost}")
        time.sleep(2) 
        print("Notificações enviadas!")

if __name__ == "__main__":
    server = rpyc.utils.server.ThreadedServer(NotificationService, port=PORT)
    print("Iniciando serviço de notificação...")
    server.start()

