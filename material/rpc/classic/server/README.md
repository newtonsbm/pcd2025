# RPyC CLASSICO

## Build da Imagem do Servidor RPyC Classico 
docker build . --tag rpyc_classic_server

## Executando container com servidor classico e mapeamento de porta
docker run -it -p 18812:18812 rpyc_classic_server

## Cliente
python rpyc_classic_client.py

# RPyC SERVICES

## Build da Imagem do Servidor RPyC Services
docker build . --tag rpyc_services_server

## Executando container com servidor services e mapeamento de porta
docker run -it -p 18811:18811 rpyc_services_server

## Cliente
python rpyc_services_client.py


