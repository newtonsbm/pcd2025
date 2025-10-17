import os
import time
import random
import rpyc

NOTIFICATION_SERVICE_HOST = os.environ.get("NOTIFICATION_SERVICE_HOST")
NOTIFICATION_SERVICE_PORT = os.environ.get("NOTIFICATION_SERVICE_PORT")

class PaymentService:

    def __init__(self, notification_service_host, notification_service_port):
        self.conn = rpyc.connect(notification_service_host, notification_service_port)

    def processar_pagamento(self, client, product, cost):
        statuses = ["sucesso", "negado", "pendente", "cancelado"]
        payment_status = random.choice(statuses)
        print("Enviando notificação para o cliente...")
        # Call the Notification Service
        self.conn.root.notificar_pagamento(client, product, payment_status, cost)
        print("Notificação enviada!")

if __name__ == "__main__":
    payment_service = PaymentService(NOTIFICATION_SERVICE_HOST, NOTIFICATION_SERVICE_PORT)
    clients = ["Mariana", "João", "Maria"]
    products = ["Café", "Pão", "Leite"]
    costs = [4.99, 2.49, 1.99]

    while True:
        client = random.choice(clients)
        product = random.choice(products)
        cost = random.choice(costs)
        payment_service.processar_pagamento(client, product, cost)
        time.sleep(3)
