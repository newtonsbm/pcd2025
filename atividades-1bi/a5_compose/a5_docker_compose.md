# Atividade A5 Docker Compose 

## Parte 1 - Aplicação web com Docker Compose

Vamos subir uma aplicação web com Docker Compose

- Instalar o docker compose (no windows já vem pre instalado veirfique com `docker compose version`)
- Utilizando o Dockerfile criado na atividade anterior (com projeto do café com pão ou com outra aplicaçao web)
- Crie um arquivo compose.yaml dentro da pasta do projeto (no mesmo local do Dockerfile) para subir o container do projeto
- Crie 1 service que representa a aplicação web
- Faça o mapeamento de portas e de volume
- Faça o build com o comando `docker compose build .`
- Suba o container com o comando `docker compose up`
- Tire um print screen da aplicação rodadno
- Suba no github o print screen da aplicação rodando juntamente com o arquivo compose.yaml criado na pasta do projeto

Arquivo de exemplo do compose:

```
services:
  web:
    build: . # local do dockerfile
    ports:
      - "3000:5000" # porta de origem para porta destino
    volumes:
      - .:/pasta_no_container # mapeamento de volume pasta origem : pasta destino
    environment: # variaveis de ambiente
      - VARIAVEL=valor
    command: ["python", "manage.py", "runserver"] # comando

```
