# Atividade A7 - Projeto de Endpoints REST: Café com Pão

Nesta atividade, você irá projetar alguns endpoints REST do **"Café com Pão"**, que oferece compra e assinatura de cestas de café da manhã em uma rede de padarias conveniadas. As entregas são realizadas por motoboys, utilizando um aplicativo de logística externo.

## Objetivos

- Compreender e aplicar conceitos de APIs RESTful.
- Projetar endpoints para operações de CRUD e filtros em uma aplicação realista.
- Refletir sobre vantagens e limitações do padrão REST.
- Em grupo de ate 3 pessoas.

## Parte 1: Discussão Conceitual

- Quais são as vantagens de se utilizar uma API RESTful em comparação a uma API não RESTful?

## Parte 2: Projeto dos Endpoints

Considere os seguintes requisitos para a API da aplicação:

- CRUD de Padarias: permitir listagem, detalhamento, cadastro, atualização e deleção de padarias.
- Filtrar padarias por cidade.
- Filtrar padarias próximas ao usuário (por localização geográfica).
- Buscar padaria por nome.
- Permitir que o usuário favorite/desfavorite padarias.

### Tarefa

1. **Liste e descreva os principais endpoints REST necessários para atender aos requisitos acima.**
   - Para cada endpoint, indique:
     - O método HTTP (GET, POST, PUT, DELETE, etc.) 
     - O caminho (URL) do endpoint
     - Uma breve descrição da funcionalidade
     - Parâmetros relevantes (query params, path params, body, etc.)

3. **Descreva como a funcionalidade de favoritar padarias pode ser modelada na API.**
4. **Crie um arquivo yaml no formato OpenAPI (Swagger) e adicione no https://editor.swagger.io/**
5. **Subir o arquivo yaml gerado no repositorio na pasta a7_rest**


## Exemplo de CRUD de Tarefas

Abaixo segue um exemplo de como descrever um CRUD simples para uma entidade "Tarefa" (Task):

- **Listar tarefas**
  - Método: GET
  - Endpoint: `/tarefas`
  - Descrição: Retorna uma lista de todas as tarefas.
  - Parâmetros: `status` (opcional, query) para filtrar tarefas por status (ex: concluída ou pendente).

- **Detalhar uma tarefa**
  - Método: GET
  - Endpoint: `/tarefas/{id}`
  - Descrição: Retorna os detalhes de uma tarefa específica.
  - Parâmetros: `id` (path)

- **Criar uma nova tarefa**
  - Método: POST
  - Endpoint: `/tarefas`
  - Descrição: Cria uma nova tarefa.
  - Parâmetros: Corpo da requisição (body) com os dados da tarefa.

- **Atualizar uma tarefa**
  - Método: PUT
  - Endpoint: `/tarefas/{id}`
  - Descrição: Atualiza os dados de uma tarefa existente.
  - Parâmetros: `id` (path), corpo da requisição (body) com os dados atualizados.

- **Deletar uma tarefa**
  - Método: DELETE
  - Endpoint: `/tarefas/{id}`
  - Descrição: Remove uma tarefa existente.
  - Parâmetros: `id` (path)

---

## Exemplo de arquivo OpenAPI (Swagger) para o CRUD de tarefas

```yaml
openapi: 3.0.0
info:
  title: API de Tarefas
  version: 1.0.0
paths:
  /tarefas:
    get:
      summary: Lista todas as tarefas
      parameters:
        - in: query
          name: status
          schema:
            type: string
            enum: [concluida, pendente]
          description: Filtra tarefas pelo status (concluida ou pendente)
      responses:
        '200':
          description: Lista de tarefas
          content:
            application/json:
              schema:
                type: array
                items:
                  $ref: '#/components/schemas/Tarefa'
    post:
      summary: Cria uma nova tarefa
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/TarefaInput'
      responses:
        '201':
          description: Tarefa criada
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Tarefa'
  /tarefas/{id}:
    get:
      summary: Detalha uma tarefa
      parameters:
        - in: path
          name: id
          required: true
          schema:
            type: integer
      responses:
        '200':
          description: Detalhes da tarefa
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Tarefa'
        '404':
          description: Tarefa não encontrada
    put:
      summary: Atualiza uma tarefa
      parameters:
        - in: path
          name: id
          required: true
          schema:
            type: integer
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/TarefaInput'
      responses:
        '200':
          description: Tarefa atualizada
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Tarefa'
        '404':
          description: Tarefa não encontrada
    delete:
      summary: Remove uma tarefa
      parameters:
        - in: path
          name: id
          required: true
          schema:
            type: integer
      responses:
        '204':
          description: Tarefa removida com sucesso
        '404':
          description: Tarefa não encontrada
components:
  schemas:
    Tarefa:
      type: object
      properties:
        id:
          type: integer
        titulo:
          type: string
        descricao:
          type: string
        concluida:
          type: boolean
    TarefaInput:
      type: object
      properties:
        titulo:
          type: string
        descricao:
          type: string
        concluida:
          type: boolean
      required:
        - titulo
```
