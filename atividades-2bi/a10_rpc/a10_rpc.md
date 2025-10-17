# Atividade A10 - RPC e gRPC

## Objetivo

Implementar comunicação entre microsserviços utilizando RPC (Remote Procedure Call) ou gRPC (Google Remote Procedure Call), aplicando conceitos de sistemas distribuídos.

## Contexto

Você irá trabalhar com o projeto **cafe-grpc** visto em aula, que demonstra a comunicação entre dois microsserviços:
- **payment_service**: Processa pagamentos e atua como cliente gRPC
- **notification_service**: Envia notificações e atua como servidor gRPC

## Opções de Implementação

Escolha **UMA** das seguintes opções:

### Opção 1: Estender o Projeto Café com Pão

Implemente um **novo serviço** que seja chamado pelo `payment_service` ou pelo `notification_service`.

**Sugestões de Serviços:**
- **Serviço de Estoque (inventory_service)**: Verificar disponibilidade de produtos
- **Serviço de Fidelidade (loyalty_service)**: Registrar pontos de fidelidade após compra
- **Serviço de Auditoria (audit_service)**: Registrar todas as transações para compliance
- **Serviço de Cupons (coupon_service)**: Validar e aplicar cupons de desconto
- **Serviço de Email (email_service)**: Enviar confirmação por email

**Arquitetura Esperada (exemplo):**
```
payment_service (cliente) 
    ↓ chama via gRPC
notification_service (servidor)

payment_service (cliente)
    ↓ chama via gRPC
seu_novo_serviço (servidor)
```

### Opção 2: Criar Novo Projeto Completo

Implemente **dois novos serviços** (cliente e servidor) relacionados a um contexto diferente do café com pão.

**Sugestões de Projetos:**
- **Sistema de Biblioteca**: `book_service` (servidor) + `library_app` (cliente)
- **Sistema de Delivery**: `restaurant_service` (servidor) + `delivery_app` (cliente)
- **Sistema Acadêmico**: `grade_service` (servidor) + `student_portal` (cliente)
- **Sistema de Streaming**: `media_service` (servidor) + `player_client` (cliente)
- **Sistema de Reservas**: `booking_service` (servidor) + `reservation_app` (cliente)

## Dicas de Implementação

### 1. Definição do Serviço (.proto)

Crie um arquivo `.proto` com:
- Pelo menos 1 serviço com 1 RPC
- Mensagens de request e response apropriadas
- Tipos de dados adequados (evite `float` para valores monetários)

### 2. Implementação do Servidor

- Implementar a classe do serviço herdando do servicer gerado
- Implementar o(s) método(s) RPC definido(s)
- Inicializar servidor gRPC na porta apropriada
- Adicionar logs informativos

### 3. Implementação do Cliente

- Criar canal de comunicação com o servidor
- Criar stub do serviço
- Fazer chamadas RPC ao servidor

### 4. Containerização

- Criar `Dockerfile` para cada serviço
- Criar `compose.yaml` com ambos os serviços
- Configurar variáveis de ambiente
- Adicionar `depends_on` para garantir ordem de inicialização
- Configurar volumes para desenvolvimento

