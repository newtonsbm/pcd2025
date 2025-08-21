# Atividade A3 Docker

- Instale o Docker
- Rode um CMS ou plataforma de blog em um container, faça o mapeamento de portas e as configurações necessárias para acessá-la pelo navegador no hospedeiro
- Coloque 1 print da plataforma sendo acessada pelo navegador do host na pasta a3_docker criada
- Faça o commit e o push com a print da ferramenta sendo acessada pelo navegador 
- Exemplos:
    - Plataformas
    - Wordpress
    - Ghost Blog
    - Joomla
    - Drupal
    - ou alguma a sua escolha
- https://hub.docker.com/search 

# Material de Apoio

## 1. Verificar instalação

```
docker --version
docker run hello-world
```

## 2. Preparação do Ambiente

- Verificar se Docker está funcionando

```bash
docker ps
```

## 3. Opções de CMS/Plataformas de Blog


### Opção 1: WordPress (Recomendado para iniciantes)

```bash
# Executar WordPress com MySQL
docker run --name wordpress-mysql -e MYSQL_ROOT_PASSWORD=rootpass -e MYSQL_DATABASE=wordpress -e MYSQL_USER=wpuser -e MYSQL_PASSWORD=wppass -d mysql:5.7

# Executar WordPress
docker run --name my-wordpress --link wordpress-mysql:mysql -p 8080:80 -e WORDPRESS_DB_HOST=mysql:3306 -e WORDPRESS_DB_USER=wpuser -e WORDPRESS_DB_PASSWORD=wppass -e WORDPRESS_DB_NAME=wordpress -d wordpress

### Opção 2: Ghost Blog

```bash
# Executar Ghost Blog
docker run --name ghost-blog -p 8080:2368 -e NODE_ENV=production -d ghost:latest

# Ou com volume persistente:
docker run --name ghost-blog -p 8080:2368 -e NODE_ENV=production -v ~/a04_docker/ghost-data:/var/lib/ghost/content -d ghost:latest
```

### Opção 3: Joomla

```bash
# Executar MySQL para Joomla
docker run --name joomla-mysql -e MYSQL_ROOT_PASSWORD=rootpass -e MYSQL_DATABASE=joomla -e MYSQL_USER=joomla -e MYSQL_PASSWORD=joomlapass -d mysql:5.7

# Executar Joomla
docker run --name my-joomla --link joomla-mysql:mysql -p 8080:80 -e JOOMLA_DB_HOST=mysql:3306 -e JOOMLA_DB_USER=joomla -e JOOMLA_DB_PASSWORD=joomlapass -e JOOMLA_DB_NAME=joomla -d joomla:latest
```

### Opção 4: Drupal

```bash
# Executar PostgreSQL para Drupal
docker run --name drupal-postgres -e POSTGRES_PASSWORD=drupalpass -e POSTGRES_DB=drupal -e POSTGRES_USER=drupal -d postgres:13

# Executar Drupal
docker run --name my-drupal --link drupal-postgres:postgres -p 8080:80 -d drupal:latest
```

## 4. Verificação e Acesso

```bash
# Verificar containers em execução
docker ps

# Verificar logs se necessário
docker logs my-wordpress  # ou nome do seu container

# Acessar no navegador
# http://localhost:8080
```

## 5. Comandos Úteis para Gerenciamento

```bash
# Parar containers
docker stop my-wordpress wordpress-mysql  # ou nomes dos seus containers

# Iniciar containers parados
docker start my-wordpress wordpress-mysql

# Remover containers (dados serão perdidos se não tiver volumes)
docker rm my-wordpress wordpress-mysql

# Listar imagens baixadas
docker images

# Remover imagens não utilizadas
docker image prune

# Ver uso de espaço
docker system df

# Limpeza geral (cuidado!)
docker system prune -a
```

## 6. Capturar Screenshot

1. Acesse `http://localhost:8080` no seu navegador
2. Complete a configuração inicial da plataforma escolhida
3. Capture um screenshot da página funcionando
4. Salve o screenshot na pasta `~/a04_docker/`
