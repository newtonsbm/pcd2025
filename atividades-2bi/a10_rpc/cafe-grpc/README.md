# Serviços em gRPC com Python

## Descrição

Este projeto é um exemplo de como criar um serviço em gRPC com Python no contexto do café com pão usando Docker e Docker Compose.

## Passo a Passo

1. Implementar o arquivo `.proto` com a definição do serviço e das mensagens.
2. Gerar o código Python a partir do arquivo `.proto`.
Supondo que o arquivo `.proto` se chame `arquivo_proto.proto`, o comando para gerar o código Python é o seguinte:
```bash
python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. arquivo_proto.proto
```
Podemos rodar esse comando com Docker e Docker Compose. Considernado que temos o servico chamado nome_do_service no docker compose e o arquivo `.proto` chamado arquivo_proto.proto, basta rodar o seguinte comando:

```bash
docker compose run nome_do_service python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. arquivo_proto.proto
```

- No exemplo nosso para gerar o arquivo do serviço de pagamento chamado `payment_service` e o arquivo .proto chamado `payment.proto`
- No exemplo nosso para gerar o arquivo do serviço de notificação chamado `notification_service` e o arquivo .proto chamado `notification.proto`

```bash
docker compose run payment_service python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. payment.proto
``` 

```bash
docker compose run notification_service python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. notification.proto
```

3. Implementar o servidor gRPC.
4. Implementar o cliente gRPC (opcional).