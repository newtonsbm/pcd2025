import pika
import json
import time
import random
import logging
from typing import Optional

class EmailConfig:
    HOST = 'rabbit'
    EXCHANGE = 'notificacoes'
    QUEUE = 'mailing'
    EXCHANGE_TYPE = 'fanout'

class EmailService:
    def __init__(self):
        self.channel: Optional[pika.channel.Channel] = None
        self.connection: Optional[pika.BlockingConnection] = None
        self._setup_logging()

    def _setup_logging(self) -> None:
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger('EmailService')

    def connect(self) -> None:
        try:
            self.connection = pika.BlockingConnection(
                pika.ConnectionParameters(host=EmailConfig.HOST)
            )
            self.channel = self.connection.channel()
            self._setup_exchange()
            self.logger.info("Successfully connected to RabbitMQ")
        except Exception as e:
            self.logger.error(f"Failed to connect to RabbitMQ: {str(e)}")
            raise

    def _setup_exchange(self) -> None:
        self.channel.exchange_declare(
            exchange=EmailConfig.EXCHANGE,
            exchange_type=EmailConfig.EXCHANGE_TYPE
        )
        result = self.channel.queue_declare(
            queue=EmailConfig.QUEUE,
            exclusive=True
        )
        self.channel.queue_bind(
            exchange=EmailConfig.EXCHANGE,
            queue=result.method.queue
        )

    def process_email(self, channel, method, properties, body: bytes) -> None:
        try:
            pedido = json.loads(body)
            self.logger.info(f"Processing email for order {pedido['id']}")
            self._simulate_email_sending(pedido)
            self.logger.info(f"Email sent successfully for order {pedido['id']}")
        except json.JSONDecodeError:
            self.logger.error("Failed to decode message body")
        except KeyError:
            self.logger.error("Message missing required 'id' field")
        except Exception as e:
            self.logger.error(f"Error processing email: {str(e)}")

    def _simulate_email_sending(self, pedido: dict) -> None:
        tempo_envio = random.randint(1, 5)
        time.sleep(tempo_envio)

    def start(self) -> None:
        self.logger.info("Starting email service...")
        try:
            self.channel.basic_consume(
                queue=EmailConfig.QUEUE,
                on_message_callback=self.process_email,
                auto_ack=True
            )
            self.channel.start_consuming()
        except KeyboardInterrupt:
            self.logger.info("Shutting down email service...")
            self.cleanup()
        except Exception as e:
            self.logger.error(f"Service error: {str(e)}")
            self.cleanup()

    def cleanup(self) -> None:
        if self.connection and not self.connection.is_closed:
            self.connection.close()
            self.logger.info("Connection closed")

def main():
    service = EmailService()
    try:
        service.connect()
        service.start()
    except Exception as e:
        logging.error(f"Failed to start service: {str(e)}")
        exit(1)

if __name__ == '__main__':
    main()