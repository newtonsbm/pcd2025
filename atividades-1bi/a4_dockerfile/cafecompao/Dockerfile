FROM python:3.11-slim  

# Definir diretório de trabalho
WORKDIR /app  
# # Copiar dependências (requirements.txt, package.json etc.)
COPY requirements.txt .  
# # Instalar dependências
RUN pip install -r requirements.txt  
# # Copiar código da aplicação
COPY . .  
# # Expor porta (ajuste de acordo com sua aplicação)
EXPOSE 8000  
# # Definir comando de inicialização (ex.: Django, Flask, Node, etc.)
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]