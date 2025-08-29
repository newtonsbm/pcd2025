# Comandos Docker 

- CLI CheatSheet: https://docs.docker.com/get-started/docker_cheatsheet.pdf 

## Geral

- `docker pull namespace/nome_imagem:nome_tag` : download da imagem a partir do DockerHub
- `docker image ls` : listar imagens Docker localmente armazenadas
- `docker run namespace/nome_image:nome_tag`: executa um container a partir de uma imagem
- `docker run -p porta_host:porta_container namespace/imagem:tag` : executa um container realizando um mapemaento de portas entre host e container (guest)
- `docker run -p porta_host:porta_container -v path/host:past/container/guest namespace/imagem:tag` : executa um container com mapeamento de portas e mapeamento de volume

### Outros exemplos

#### Build
- `docker build -t nome_da_imagem:tag .` : constrói uma imagem a partir de um Dockerfile no diretório atual
- `docker build -t minha_app:v1.0 .` : exemplo de build com nome específico e tag

#### Execução e gerenciamento
- `docker ps` : lista containers em execução
- `docker ps -a` : lista todos os containers (incluindo parados)
- `docker stop container_id` : para um container em execução
- `docker rm container_id` : remove um container parado
- `docker rmi image_id` : remove uma imagem
- `docker exec -it container_id /bin/bash` : acessa o terminal de um container em execução

#### Executar com display compartilhado

**Linux:**
- `docker run -e DISPLAY=$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix namespace/imagem:tag` : executa container com acesso ao display X11 do host
- `docker run --privileged -e DISPLAY=$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix namespace/imagem:tag` : executa com privilégios elevados para aplicações gráficas

**Windows:**
- Instalar um servidor X11 como VcXsrv ou Xming
- `docker run -e DISPLAY=host.docker.internal:0.0 namespace/imagem:tag` : executa container com acesso ao display através do servidor X11
- `docker run --privileged -e DISPLAY=host.docker.internal:0.0 namespace/imagem:tag` : executa com privilégios elevados

**Mac:**
- Instalar XQuartz (`brew install --cask xquartz`)
- Configurar XQuartz para permitir conexões de rede: `xhost +localhost`
- `docker run -e DISPLAY=host.docker.internal:0 namespace/imagem:tag` : executa container com acesso ao display através do XQuartz
- `docker run --privileged -e DISPLAY=host.docker.internal:0 namespace/imagem:tag` : executa com privilégios elevados


#### Logs e debug
- `docker logs container_id` : visualiza os logs de um container
- `docker inspect container_id` : exibe informações detalhadas sobre um container

#### Limpeza
- `docker system prune` : remove containers parados, redes não utilizadas e imagens órfãs
- `docker container prune` : remove apenas containers parados
- `docker image prune` : remove apenas imagens órfãs
