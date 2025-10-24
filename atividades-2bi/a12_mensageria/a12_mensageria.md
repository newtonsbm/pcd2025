# A12 - Mensageria

## Objetivo

Baseando-se no exemplo visto em aula, implemente dois novos serviços integrados ao mecanismo de mensageria do RabbitMQ.

## Tarefas

### 1. Serviço de Envio de SMS

- **Descrição**: Criar um serviço de envio de SMS seguindo o mesmo padrão dos serviços de WhatsApp e Mailing já existentes
- **Requisitos**:
  - Deve consumir da mesma fila que os serviços anteriores (padrão pub/sub)
  - Simular o processo de envio de SMS
  - Seguir a estrutura e padrões dos outros consumers

### 2. Serviço de Geração de Nota Fiscal

- **Descrição**: Criar um novo serviço responsável pela geração de notas fiscais
- **Requisitos**:
  - Criar um Consumer que irá gerar a nota fiscal
  - Seguir o padrão dos outros consumers, porém utilizando uma **fila simples** (work queue)
  - Alterar o Producer (serviço `cafepao`) para publicar esse novo evento ("gerar nota fiscal")
  - O Consumer deverá consumir as mensagens dessa nova fila

## Entrega

Faça o commit e suba no github classroom