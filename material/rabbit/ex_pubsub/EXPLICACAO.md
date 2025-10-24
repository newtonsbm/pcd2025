# Explicação Detalhada - Padrão Pub/Sub

## Introdução

O padrão **Publish/Subscribe (Pub/Sub)** é um modelo de comunicação onde os produtores de mensagens (publishers) não enviam mensagens diretamente para consumidores específicos (subscribers). Em vez disso, as mensagens são publicadas em um **exchange**, e os subscribers interessados recebem cópias dessas mensagens.

## Conceitos Fundamentais

### 1. Exchange Fanout

```python
channel.exchange_declare(
    exchange='pedidos_pizzaria',
    exchange_type='fanout',  # Tipo fanout = broadcast
    durable=True
)
```

O exchange do tipo **fanout** funciona como um **broadcast**:
- Ignora routing keys
- Envia mensagem para TODAS as filas conectadas a ele
- Cada fila recebe uma CÓPIA da mensagem

### 2. Filas Exclusivas

```python
result = channel.queue_declare(queue='', exclusive=True)
queue_name = result.method.queue
```

Características:
- `queue=''`: Nome gerado automaticamente pelo RabbitMQ (ex: `amq.gen-xyz`)
- `exclusive=True`: Apenas esta conexão pode usar a fila
- Fila é automaticamente deletada quando a conexão fecha

### 3. Binding

```python
channel.queue_bind(
    exchange='pedidos_pizzaria',
    queue=queue_name
)
```

O **binding** conecta uma fila ao exchange. A partir desse momento, todas as mensagens publicadas no exchange são copiadas para esta fila.

## Fluxo de Comunicação

```
PUBLISHER                        EXCHANGE FANOUT              SUBSCRIBERS
                                                             
   🍕                              pedidos_pizzaria
Sistema de                                                    
 Pedidos                                                      
    │                                    │                    
    │ publish()                          │                    
    └────────────────────────────────────┤                    
                                         │                    
                              ┌──────────┼──────────┬─────────────┐
                              │          │          │             │
                              ▼          ▼          ▼             ▼
                         [Queue 1]  [Queue 2]  [Queue 3]    [Queue 4]
                              │          │          │             │
                              ▼          ▼          ▼             ▼
                          👨‍🍳        🏍️        📱          💰
                        Cozinha   Entregador    App      Financeiro
```

## Comparação com Outros Padrões

### Pub/Sub vs Work Queue

**Work Queue (Pipeline)**:
```
Publisher → Queue → [Worker 1, Worker 2, Worker 3]
                    ↑ Apenas UM worker processa a mensagem
```

**Pub/Sub**:
```
Publisher → Exchange → [Sub 1, Sub 2, Sub 3, Sub 4]
                       ↑ TODOS os subscribers recebem a mensagem
```

### Quando usar cada um?

#### Use **Work Queue** quando:
- Você quer distribuir TRABALHO entre workers
- Cada tarefa deve ser executada UMA vez apenas
- Exemplo: Processar uploads de imagens

#### Use **Pub/Sub** quando:
- Você quer NOTIFICAR múltiplos serviços
- Cada serviço faz uma ação diferente
- Exemplo: Notificar pedido (cozinha prepara, app notifica, financeiro registra)

## Código Comentado

### Publisher

```python
def publicar_pedido(channel, pedido):
    """Publica no EXCHANGE, não em uma fila específica."""
    mensagem = json.dumps(pedido)
    
    # Publica no exchange
    channel.basic_publish(
        exchange='pedidos_pizzaria',  # Nome do exchange
        routing_key='',               # Vazio! Fanout ignora routing keys
        body=mensagem,
        properties=pika.BasicProperties(
            delivery_mode=2,  # Mensagem persistente
        )
    )
```

Pontos importantes:
- Publica no **exchange**, não em fila
- `routing_key=''`: Fanout ignora isso
- Publisher não sabe quantos/quais subscribers existem

### Subscriber

```python
def main():
    # 1. Declara o exchange (idempotente)
    channel.exchange_declare(
        exchange='pedidos_pizzaria',
        exchange_type='fanout',
        durable=True
    )
    
    # 2. Cria fila exclusiva e temporária
    result = channel.queue_declare(queue='', exclusive=True)
    queue_name = result.method.queue
    
    # 3. Faz o binding: conecta fila ao exchange
    channel.queue_bind(
        exchange='pedidos_pizzaria',
        queue=queue_name
    )
    
    # 4. Consome mensagens da sua fila
    channel.basic_consume(
        queue=queue_name,
        on_message_callback=callback,
        auto_ack=True
    )
    
    channel.start_consuming()
```

Pontos importantes:
- Cada subscriber cria sua PRÓPRIA fila
- Todas as filas recebem CÓPIAS das mensagens
- Subscribers não sabem da existência uns dos outros

## Exemplo Prático: Pizzaria

### Cenário
Um cliente faz um pedido de pizza. O que acontece?

1. **Publisher** (Sistema de Pedidos):
   ```python
   pedido = {
       'numero': 1,
       'cliente': 'João',
       'pizza': 'Calabresa',
       'preco': 38.00
   }
   publicar_pedido(channel, pedido)
   ```

2. **Exchange** recebe e distribui para TODAS as filas

3. **Subscribers** recebem o mesmo pedido:
   
   **Cozinha**:
   ```
   🔔 Novo pedido! Preparando 1x Calabresa...
   ✓ Pizza pronta!
   ```
   
   **Entregador**:
   ```
   📦 Novo pedido para entrega
   🏍️ Moto 1 designada
   ⏱️ Tempo estimado: 25 minutos
   ```
   
   **App**:
   ```
   📱 Enviando notificação para João
   📧 Email: Pedido #001 confirmado
   ```
   
   **Financeiro**:
   ```
   💰 Venda registrada: R$ 38.00
   📊 Faturamento acumulado: R$ 38.00
   ```

## Vantagens do Pub/Sub

✅ **Desacoplamento**: Publisher não conhece subscribers  
✅ **Escalabilidade**: Adicione subscribers sem alterar publisher  
✅ **Flexibilidade**: Cada subscriber faz o que quiser com a mensagem  
✅ **Broadcast**: Notifique múltiplos serviços simultaneamente

## Desvantagens

⚠️ **Overhead**: Múltiplas cópias da mesma mensagem  
⚠️ **Processamento redundante**: Se não for intencional  
⚠️ **Complexidade**: Mais partes para gerenciar  
⚠️ **Debug**: Rastrear fluxo entre múltiplos serviços

## Casos de Uso Reais

### E-commerce
```
Pedido confirmado →
  ├─ Estoque: Reserva produtos
  ├─ Pagamento: Processa cobrança
  ├─ Logística: Prepara envio
  ├─ Email: Notifica cliente
  └─ Analytics: Registra conversão
```

### Redes Sociais
```
Nova postagem →
  ├─ Timeline: Atualiza feed
  ├─ Notificações: Alerta seguidores
  ├─ Search: Indexa conteúdo
  ├─ Analytics: Conta engajamento
  └─ Cache: Invalida cache
```

### IoT/Sensores
```
Sensor detecta movimento →
  ├─ Câmera: Inicia gravação
  ├─ Alarme: Dispara alerta
  ├─ App: Notifica proprietário
  └─ Log: Registra evento
```

## Testando o Exemplo

### 1. Inicie o sistema
```bash
docker-compose up
```

### 2. Observe os logs
Cada serviço mostrará sua perspectiva do mesmo pedido:
```bash
# Ver apenas a cozinha
docker-compose logs -f cozinha

# Ver apenas financeiro
docker-compose logs -f financeiro
```

### 3. Escale subscribers
```bash
# Inicie 3 entregadores
docker-compose up --scale entregador=3
```

Note que TODOS os 3 entregadores receberão TODOS os pedidos!

### 4. Acesse RabbitMQ Management
http://localhost:8080 (guest/guest)

Observe:
- Exchange `pedidos_pizzaria` do tipo fanout
- Múltiplas filas conectadas ao exchange
- Cada mensagem sendo replicada

## Evolução: Pub/Sub com Filtros

Este exemplo usa **fanout** (broadcast total). Para filtrar mensagens, você pode evoluir para:

### Topic Exchange
```python
# Publisher
channel.basic_publish(
    exchange='pedidos',
    routing_key='pedidos.urgente',  # Chave de roteamento
    body=mensagem
)

# Subscriber
channel.queue_bind(
    exchange='pedidos',
    queue=queue_name,
    routing_key='pedidos.urgente'  # Só recebe pedidos urgentes
)
```

### Direct Exchange
```python
# Roteamento exato por chave
channel.basic_publish(
    exchange='logs',
    routing_key='error',  # Nível de log
    body=log_message
)
```

## Referências

- [RabbitMQ Tutorial 3 - Pub/Sub](https://www.rabbitmq.com/tutorials/tutorial-three-python.html)
- [Exchange Types](https://www.rabbitmq.com/tutorials/amqp-concepts.html#exchanges)
- [Pika Documentation](https://pika.readthedocs.io/)

