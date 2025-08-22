# Atividade A4 Dockerfile

Nesta atividade, você vai praticar a criação de **imagens Docker** e a execução de uma aplicação web dentro de um **container**.

## Objetivos

* Criar um `Dockerfile` para empacotar uma aplicação web simples.
* Rodar a aplicação dockerizada e acessá-la via navegador.
* Explorar recursos extras como compartilhamento em rede e volumes.

---

## Instruções

1. **Escolha o projeto**

   * Você pode reutilizar o projeto do semestre anterior (aplicação Django “Café com Pão”, opcional).
   * Caso não tenha, crie um novo projeto web em qualquer linguagem/framework (ex.: Django, Flask, Node.js, FastAPI, etc.).
   * O projeto pode ser apenas o **starter-code** (não precisa estar 100% funcional).

2. **Crie o `Dockerfile`**

   * Escreva um `Dockerfile` que:

     * Defina a imagem base adequada.
     * Copie os arquivos do projeto para dentro da imagem.
     * Instale dependências necessárias.
     * Defina o comando para iniciar a aplicação.

   **Exemplo de apoio:**

   ```dockerfile
   # Escolha da imagem base
   FROM python:3.11-slim  

   # Definir diretório de trabalho
   WORKDIR /app  

   # Copiar dependências (requirements.txt, package.json etc.)
   COPY requirements.txt .  

   # Instalar dependências
   RUN pip install -r requirements.txt  

   # Copiar código da aplicação
   COPY . .  

   # Expor porta (ajuste de acordo com sua aplicação)
   EXPOSE 8000  

   # Definir comando de inicialização (ex.: Django, Flask, Node, etc.)
   CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
   ```

3. **Build e execução do container**

   * Crie a imagem com:

     ```bash
     docker build -t cafecompao .
     ```
   * Rode o container mapeando a porta:

     ```bash
     docker run -p 8000:8000 cafecompao 
     ```
   * Acesse no navegador:

     ```
     http://localhost:8000
     ```

4. **Entrega mínima**

   * Suba o arquivo `Dockerfile` criado nesta pasta.
   * Inclua um **print da tela do navegador** mostrando sua aplicação rodando.

---

## Desafios (Plus)

1. **Compartilhamento em rede**

   * Conecte-se à rede Wi-Fi disponibilizada em sala.
   * Rode o container e compartilhe o **IP da sua máquina + porta** para que colegas testem no navegador.

2. **Volumes**

   * Configure um **volume** para mapear os arquivos locais do projeto para dentro do container.
   * Teste editando o código no host e veja a atualização refletida no container.
   * Exemplo parcial:

     ```bash
     docker run -p 8000:8000 -v $(pwd):/app cafecompao
     ```

3. **Tamanho da imagem**

   * Verifique o tamanho da sua imagem com:

     ```bash
     docker images
     ```
   * Inclua um print mostrando o tamanho da imagem no seu documento final.


