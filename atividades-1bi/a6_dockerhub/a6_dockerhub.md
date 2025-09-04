# A6: Publicando uma imagem no Docker Hub

Nesta atividade, vamos aprender a construir uma imagem Docker de uma aplicação, publicá-la no Docker Hub e, em seguida, usá-la em um arquivo Docker Compose.

## Passos

### 1. Crie uma conta no Docker Hub

Se você ainda não tiver uma, acesse o [Docker Hub](https://hub.docker.com/) e crie uma conta gratuita. O seu nome de usuário será usado para identificar suas imagens.

### 2. Crie um repositório no Docker Hub

No painel do Docker Hub, crie um novo repositório. Você pode dar a ele o nome que preferir, por exemplo, `cafecompao`.


### 3. Prepare sua aplicação

Para esta atividade, vamos usar um projeto Django simples. Se você não tiver um, pode usar o exemplo do `cafecompao` que usamos em aulas anteriores. Certifique-se de que ele tenha um `Dockerfile` e um `compose.yml`.

Exemplo de `Dockerfile`:

```dockerfile
# Use uma imagem base do Python
FROM python:3.13-slim

# Defina o diretório de trabalho
WORKDIR /app

# Copie os arquivos de dependências
COPY requirements.txt .

# Instale as dependências
RUN pip install -r requirements.txt

# Copie o resto do código da aplicação
COPY . .

# Exponha a porta que a aplicação vai usar
EXPOSE 8000

# Comando para rodar a aplicação
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
```

### 4. Faça o login no Docker via terminal

Antes de enviar a imagem, você precisa se autenticar no Docker Hub pelo seu terminal. Use o comando:

```bash
docker login
```

Ele pedirá seu nome de usuário e senha do Docker Hub.

### 5. Crie um arquivo `compose.yml`

Crie um arquivo `compose.yml` (caso nao exista) para definir o serviço da sua aplicação. A parte mais importante é o nome da `image`. Ele deve seguir o formato: `<seu-usuario-dockerhub>/<nome-do-repositorio>:<tag>`.

Aqui está um exemplo de `compose.yml`:

```yaml

services:
  web:
    build: .
    image: seu-usuario-dockerhub/meu-app-django:latest # <-- Altere para o seu usuário e nome do repositório que desejar
    command: python manage.py runserver 0.0.0.0:8000
    volumes:
      - .:/app
    ports:
      - "8000:8000"
```

### 6. Construa e envie a imagem

Com o `compose.yml` configurado, use os seguintes comandos:

1.  **Construir a imagem:** Este comando irá ler o `Dockerfile` no diretório atual (`.`), construir a imagem e nomeá-la de acordo com o que foi definido no campo `image` do `compose.yml`.

    ```bash
    docker compose build
    ```

2.  **Enviar a imagem para o Docker Hub:** Após a construção, este comando envia a imagem para o seu repositório no Docker Hub.

    ```bash
    docker compose push
    ```

### 7. Verifique no Docker Hub

Acesse seu repositório no Docker Hub e verifique se a imagem com a tag `latest` foi enviada com sucesso.

## Entrega

Na pasta `a6_dockerhub` no seu repositório de atividades e envie:

1.  O arquivo `compose.yml` que você criou.
2.  Um print da tela do seu Docker Hub mostrando a imagem publicada no seu repositório.
3.  Um link para o repositório do Docker Hub onde a imagem está publicada num arquivo README.md.

plus: pegue o link do repositório do Docker Hub de um colega de classe e rode a imagem dele localmente usando o docker, veja se funciona corretamente.

