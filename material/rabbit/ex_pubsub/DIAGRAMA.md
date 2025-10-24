# Diagrama Visual - Pizzaria Digital (Pub/Sub)

## Arquitetura Completa

```
┌─────────────────────────────────────────────────────────────────────────┐
│                          PIZZARIA DIGITAL                                │
│                    Padrão Publish/Subscribe (Fanout)                     │
└─────────────────────────────────────────────────────────────────────────┘

                         ┌──────────────────────┐
                         │   Sistema de Pedidos │
                         │     (Publisher)      │
                         │                      │
                         │  - Gera pedidos      │
                         │  - Publica no        │
                         │    exchange          │
                         └──────────┬───────────┘
                                    │
                                    │ publish(pedido)
                                    ▼
                         ┌──────────────────────┐
                         │  Exchange: fanout    │
                         │  "pedidos_pizzaria"  │
                         │                      │
                         │  Tipo: FANOUT        │
                         │  (Broadcast para     │
                         │   todas as filas)    │
                         └──────────┬───────────┘
                                    │
                 ┌──────────────────┼──────────────────┬──────────────┐
                 │                  │                  │              │
         binding │          binding │          binding │      binding │
                 ▼                  ▼                  ▼              ▼
          ┌──────────┐       ┌──────────┐      ┌──────────┐   ┌──────────┐
          │ Queue 1  │       │ Queue 2  │      │ Queue 3  │   │ Queue 4  │
          │(exclusiva)│       │(exclusiva)│      │(exclusiva)│   │(exclusiva)│
          └────┬─────┘       └────┬─────┘      └────┬─────┘   └────┬─────┘
               │                  │                  │              │
               │ consume          │ consume          │ consume      │ consume
               ▼                  ▼                  ▼              ▼
       ┌──────────────┐   ┌──────────────┐  ┌──────────────┐ ┌──────────────┐
       │   👨‍🍳 Cozinha │   │🏍️ Entregador │  │  📱 App      │ │ 💰 Financeiro│
       │              │   │              │  │              │ │              │
       │ - Prepara    │   │ - Organiza   │  │ - Notifica   │ │ - Registra   │
       │   pizza      │   │   entregas   │  │   cliente    │ │   vendas     │
       │              │   │ - Calcula    │  │ - SMS/Push   │ │ - Calcula    │
       │              │   │   rotas      │  │ - Email      │ │   faturamento│
       └──────────────┘   └──────────────┘  └──────────────┘ └──────────────┘
```

## Fluxo de um Pedido

```
Passo 1: Cliente faz pedido
════════════════════════════

    📱 Cliente                    🍕 Sistema
                                 
    "1x Calabresa"     ───────►  {
                                    numero: 1,
                                    pizza: "Calabresa",
                                    preco: 38.00,
                                    cliente: "João"
                                 }


Passo 2: Publicação no Exchange
════════════════════════════════

    🍕 Sistema de Pedidos
         │
         │ basic_publish(exchange='pedidos_pizzaria', ...)
         ▼
    ┌─────────────────┐
    │  Exchange       │
    │  (fanout)       │
    │                 │
    │  📢 BROADCAST   │
    └─────────────────┘


Passo 3: Distribuição para TODAS as filas
══════════════════════════════════════════

    ┌─────────────────┐
    │  Exchange       │
    │  (fanout)       │
    └────────┬────────┘
             │
    ┌────────┼────────┬────────┬────────┐
    │        │        │        │        │
    ▼        ▼        ▼        ▼        ▼
  [Q1]    [Q2]    [Q3]    [Q4]    ...
  cópia   cópia   cópia   cópia


Passo 4: Cada subscriber processa
══════════════════════════════════

👨‍🍳 Cozinha:
   ┌─────────────────────────────┐
   │ 🔔 Novo pedido!             │
   │ 👨‍🍳 Preparando Calabresa...  │
   │ ✓ Pizza pronta!             │
   └─────────────────────────────┘

🏍️ Entregador:
   ┌─────────────────────────────┐
   │ 📦 Novo pedido para entrega │
   │ 🏍️ Moto 1 designada         │
   │ ⏱️ Tempo: 25 minutos         │
   └─────────────────────────────┘

📱 App:
   ┌─────────────────────────────┐
   │ 📱 Enviando notificações    │
   │ SMS: "Pedido confirmado!"   │
   │ 📧 Email enviado            │
   └─────────────────────────────┘

💰 Financeiro:
   ┌─────────────────────────────┐
   │ 💵 Venda registrada         │
   │ Valor: R$ 38.00             │
   │ 📊 Faturamento: R$ 38.00    │
   └─────────────────────────────┘
```

## Comparação: Pub/Sub vs Work Queue

```
┌─────────────────────────────────────────────────────────────────┐
│                         WORK QUEUE                               │
│                  (Uma mensagem = Um worker)                      │
└─────────────────────────────────────────────────────────────────┘

    Producer
       │
       │ send(tarefa)
       ▼
    ┌──────┐
    │Queue │
    └───┬──┘
        │
    ┌───┴───────────┬────────────┐
    │               │            │
    ▼               ▼            ▼
 Worker 1       Worker 2     Worker 3
    │
    └─► Apenas UM worker processa cada tarefa


┌─────────────────────────────────────────────────────────────────┐
│                         PUB/SUB                                  │
│             (Uma mensagem = TODOS os subscribers)                │
└─────────────────────────────────────────────────────────────────┘

    Publisher
       │
       │ publish(evento)
       ▼
   ┌──────────┐
   │ Exchange │
   │ (fanout) │
   └────┬─────┘
        │
    ┌───┴───────────┬────────────┐
    │               │            │
    ▼               ▼            ▼
  Sub 1           Sub 2        Sub 3
    │               │            │
    └───────────────┴────────────┴─► TODOS recebem CÓPIAS
```

## Exchange Fanout - Analogia Real

```
┌────────────────────────────────────────────────────────┐
│  ANALOGIA: RÁDIO TRANSMITINDO                          │
└────────────────────────────────────────────────────────┘

       📡 Torre de Transmissão
           (Exchange Fanout)
              │
              │ Sinal de rádio
              │ (broadcast)
              │
    ┌─────────┼─────────┬─────────┬─────────┐
    │         │         │         │         │
    ▼         ▼         ▼         ▼         ▼
   📻        📻        📻        📻        📻
  Rádio 1  Rádio 2  Rádio 3  Rádio 4  Rádio 5

TODOS os rádios sintonizados na frequência
recebem o MESMO sinal!


┌────────────────────────────────────────────────────────┐
│  ANALOGIA: NEWSLETTER POR EMAIL                         │
└────────────────────────────────────────────────────────┘

       ✉️ Sistema de Newsletter
           (Publisher)
              │
              │ Envia email
              ▼
         📨 Servidor
         (Exchange)
              │
    ┌─────────┼─────────┬─────────┬─────────┐
    │         │         │         │         │
    ▼         ▼         ▼         ▼         ▼
   📧        📧        📧        📧        📧
  João    Maria    Pedro    Ana     Carlos

TODOS os inscritos recebem a MESMA newsletter!
```

## Containers e Network

```
┌──────────────────────────────────────────────────────────────┐
│                    Docker Network                             │
│                   "pizzaria-network"                          │
│                                                               │
│  ┌─────────────┐                                             │
│  │   rabbit    │ ◄─── porta 5672 (AMQP)                      │
│  │  RabbitMQ   │ ◄─── porta 8080 (Management)                │
│  └──────┬──────┘                                             │
│         │                                                     │
│         │ amqp://rabbit:5672                                 │
│         │                                                     │
│  ┌──────┴──────────────────────────────────┐                │
│  │      │        │         │        │       │                │
│  │      │        │         │        │       │                │
│  ▼      ▼        ▼         ▼        ▼       ▼                │
│ ┌────┐┌────┐  ┌────┐   ┌────┐  ┌────────┐ ...              │
│ │pub ││coz │  │ent │   │app │  │financ  │                   │
│ │    ││    │  │    │   │    │  │        │                   │
│ └────┘└────┘  └────┘   └────┘  └────────┘                   │
│                                                               │
└──────────────────────────────────────────────────────────────┘

Todos os containers se comunicam através da network interna!
```

## Timeline de Mensagens

```
t=0s    Publisher: Pedido #001 gerado
        └─► Exchange recebe

t=0.1s  Exchange: Distribui para 4 filas
        ├─► Fila da Cozinha
        ├─► Fila do Entregador  
        ├─► Fila do App
        └─► Fila do Financeiro

t=0.2s  Subscribers começam a processar (em paralelo!)
        ├─► Cozinha: "Preparando..."
        ├─► Entregador: "Calculando rota..."
        ├─► App: "Enviando SMS..."
        └─► Financeiro: "Registrando venda..."

t=3s    Cozinha: "Pizza pronta!"

t=5s    Publisher: Pedido #002 gerado
        └─► (ciclo se repete)
```

## Escalonamento

```
Sem escalonamento (padrão):
════════════════════════════
    Exchange
       │
    ┌──┴──┬──┬──┐
    ▼     ▼  ▼  ▼
    C     E  A  F

    C=Cozinha, E=Entregador, A=App, F=Financeiro
    (4 subscribers, 4 filas)


Com escalonamento (--scale entregador=3):
═════════════════════════════════════════
    Exchange
       │
    ┌──┴──┬──┬──┬──┬──┐
    ▼     ▼  ▼  ▼  ▼  ▼
    C     E1 E2 E3 A  F

    (6 subscribers, 6 filas)
    TODOS os 3 entregadores recebem TODAS as mensagens!
    (Em pub/sub isso pode não ser desejado)
```

## Referência Visual de Símbolos

```
🍕 Sistema de Pedidos     👨‍🍳 Cozinha
🏍️ Entregador             📱 App de Notificações  
💰 Financeiro             📦 Pedido
🔔 Notificação            ✓ Confirmação
📧 Email                  📱 SMS
💵 Dinheiro               📊 Estatísticas
```

