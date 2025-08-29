# A5 – Compose com Banco de Dados

Nesta atividade, você irá configurar uma aplicação web para rodar com um banco de dados isolado utilizando **Docker Compose**.

Você deverá utilizar uma aplicação Django com Docker Compose já configurado (sem banco de dados isolado) ou o projeto **Café com Pão** como base.

Seu objetivo é modificar o ambiente para incluir um serviço de banco de dados PostgreSQL de forma adequada.

---

## **Passos para Realização**

1. **Escolha da Base**

   * Utilize a aplicação Django que você já tem com o `docker-compose` básico **ou**
   * Utilize como base o projeto **Café com Pão (Django)**.

2. **Configuração do Compose**

   * Crie um serviço para o banco de dados no arquivo `compose.yaml`.
   * Adicione as **variáveis de ambiente** necessárias para o banco de dados (usuário, senha, nome do banco etc.).
   * Configure um **volume** persistente para armazenar os dados do banco.
   * Estabeleça a **dependência** entre o serviço do Django e o serviço do banco de dados com `depends_on`.

Exemoplo:

```
services:

  db:
    image: postgres:15
    volumes:
      - postgres_data:/var/lib/postgresql/data
    environment:
      - POSTGRES_DB=meubanco
      - POSTGRES_USER=meuusuario
      - POSTGRES_PASSWORD=minhasenha

volumes:
  postgres_data:
```

3. **Ajustes no Django**

   * Atualize o arquivo `settings.py` do Django para se conectar ao banco de dados através das variáveis de ambiente.

```
# arquivo settings.py

import os


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME'),
        'USER': os.environ.get('DB_USER'),
        'PASSWORD': os.environ.get('DB_PASSWORD'),
        'HOST': os.environ.get('DB_HOST'),
        'PORT': os.environ.get('DB_PORT', '5432'),
    }
}
```

   * **Atenção**: o **hostname** do banco deve ser o mesmo nome do serviço definido no `docker-compose.yaml`.

4. **Dependências**

   * Inclua o pacote `psycopg2` no arquivo de `requirements.txt` do django para que o `Dockerfile` da aplicação Django possa instalar

5. **Build e Execução**

   * Faça o build da aplicação com:

     ```bash
     docker compose build
     ```

   * Suba os containers com:

     ```bash
     docker compose up
     ```

6. **Entrega**

   * Suba no GitHub a versão atualizada do seu projeto com:

     * O novo `compose.yaml`
     * O `requirements.txt` ou `Dockerfile` atualizado
     * O `settings.py` configurado para o banco de dados
     * Na pasta a5_compose_banco

---

## **Observações Importantes**

* O **nome do serviço do banco** no `compose.yaml` será utilizado como **hostname** na configuração do Django.
* Certifique-se de que a aplicação está funcional com o banco de dados isolado antes de subir o código no GitHub.
* Voce pode rodar o comando `python manage.py migrate` para atualizar o banco de dados
