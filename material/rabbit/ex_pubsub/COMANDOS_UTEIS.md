# Comandos Úteis - Pizzaria Digital

## Iniciar e Parar

### Iniciar todos os serviços
```bash
docker-compose up
```

### Iniciar em background (detached)
```bash
docker-compose up -d
```

### Parar todos os serviços
```bash
docker-compose down
```

### Parar e remover volumes
```bash
docker-compose down -v
```

## Logs

### Ver logs de todos os serviços
```bash
docker-compose logs
```

### Seguir logs em tempo real
```bash
docker-compose logs -f
```

### Ver logs de um serviço específico
```bash
docker-compose logs -f cozinha
docker-compose logs -f entregador
docker-compose logs -f app
docker-compose logs -f financeiro
docker-compose logs -f publisher
```

### Ver últimas 50 linhas
```bash
docker-compose logs --tail=50
```

## Escalar Serviços

### Iniciar múltiplas instâncias de um serviço
```bash
# 3 entregadores
docker-compose up --scale entregador=3

# 2 cozinhas
docker-compose up --scale cozinha=2
```

**Importante**: No pub/sub, TODAS as instâncias receberão TODAS as mensagens!

## Executar Comandos em Containers

### Entrar no container
```bash
docker-compose exec cozinha bash
docker-compose exec publisher bash
```

### Executar comando Python
```bash
docker-compose exec cozinha python -c "print('Hello')"
```

## Rebuild

### Reconstruir imagens
```bash
docker-compose build
```

### Reconstruir e iniciar
```bash
docker-compose up --build
```

### Reconstruir apenas um serviço
```bash
docker-compose build cozinha
```

## Inspecionar

### Listar containers
```bash
docker-compose ps
```

### Ver configuração final do compose
```bash
docker-compose config
```

### Ver uso de recursos
```bash
docker stats
```

## RabbitMQ Management

### Acessar interface web
```
URL: http://localhost:8080
Usuário: guest
Senha: guest
```

### Ver filas via CLI
```bash
docker-compose exec rabbit rabbitmqctl list_queues
```

### Ver exchanges via CLI
```bash
docker-compose exec rabbit rabbitmqctl list_exchanges
```

### Ver bindings via CLI
```bash
docker-compose exec rabbit rabbitmqctl list_bindings
```

## Debug

### Ver variáveis de ambiente de um serviço
```bash
docker-compose exec cozinha env
```

### Testar conectividade com RabbitMQ
```bash
docker-compose exec cozinha ping rabbit
```

### Ver processos em um container
```bash
docker-compose exec cozinha ps aux
```

## Limpeza

### Remover containers parados
```bash
docker-compose rm
```

### Remover imagens não utilizadas
```bash
docker image prune
```

### Limpar tudo (cuidado!)
```bash
docker system prune -a
```

## Testes Interessantes

### Teste 1: Parar um subscriber
```bash
# Para a cozinha
docker-compose stop cozinha

# Observe que os outros continuam recebendo pedidos
docker-compose logs -f app

# Reinicie a cozinha
docker-compose start cozinha
```

### Teste 2: Múltiplos entregadores
```bash
# Inicie com 3 entregadores
docker-compose up --scale entregador=3

# Todos receberão os mesmos pedidos!
```

### Teste 3: Adicionar subscriber dinamicamente
```bash
# Em um terminal
docker-compose up

# Em outro terminal
docker-compose up --scale entregador=2
```

### Teste 4: Monitorar RabbitMQ
```bash
# Abra o RabbitMQ Management
# http://localhost:8080

# Vá em Exchanges → pedidos_pizzaria
# Observe os bindings e as mensagens
```

## Desenvolvimento

### Editar código e reiniciar
Como os volumes estão mapeados, você pode editar o código e reiniciar apenas o serviço:

```bash
# Edite o arquivo
vim cozinha/main.py

# Reinicie apenas a cozinha
docker-compose restart cozinha
```

### Reconstruir após mudar requirements
```bash
docker-compose build cozinha
docker-compose up cozinha
```

## Performance

### Ver consumo de recursos
```bash
docker stats $(docker-compose ps -q)
```

### Limitar recursos de um serviço
Edite o `compose.yaml`:
```yaml
cozinha:
  deploy:
    resources:
      limits:
        cpus: '0.5'
        memory: 512M
```

