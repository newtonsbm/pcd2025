# A2 - Virtualização 

## Parte 1

- Instalar VirtualBox
- Instalar uma distro linux leve
    - Versão com interface: puppylinux, damn small linux, antix linux ou outra bem leve
    - Versão para servidor: alpine linux (extended version), debian server, ubuntu server (pesado)
- Tirar um print e salvar no repositorio com o nome "virtualbox.jpg" na pasta a2_virtualizacao
- Comitar e subir

### Plus
- Configure port forwarding
- Instale um servidor web ou uma aplicacao web starter (ex: projeto django inicial que vimos em web)

## Parte 2
- Instalar Vagrant
- Entrar na pasta pelo terminal atividades-1bi/a2_virtualizacao
- Iniciar o projeto Vagrant com os comandos

`vagrant init generic/alpine318` 

- Configurar a porta  descomentando a linha: 
`config.vm.network "forwarded_port", guest: 8000, host: 5000`

- Iniciar vagrant
`vagrant up`

- Acessar a maquina virtual via ssh com
`vagrant ssh`

- Uma vez no container, instale o python e djagno com os comandos

`sudo apk add python3`
`sudo apk add py3-pip`

- Instalar django e inicar projeto
`pip install django`
`python3 -m django startproject teste`

- Entrar na pasta e iniciar o servidor
`cd teste`
`python manage.py run_server 0.0.0.0:8000`

- Acessar localhost:8000 no navegador do host

### Plus

- Utilize o provisionamento para instalar python automaticamente 
- Tente outro box e instale uma ferramenta diferente
- Suba os testes em um outro Vagrantfile
