#!/bin/bash

echo "=========================================="
echo "  🍕 Pizzaria Digital - Pub/Sub Demo"
echo "=========================================="
echo ""

# Para containers anteriores se existirem
echo "[1/3] Parando containers anteriores..."
docker-compose down 2>/dev/null

echo ""
echo "[2/3] Construindo imagens..."
docker-compose build

echo ""
echo "[3/3] Iniciando serviços..."
echo ""
echo "Serviços disponíveis:"
echo "  - RabbitMQ Management: http://localhost:8080"
echo "  - Publisher: Sistema de Pedidos"
echo "  - Subscribers: Cozinha, Entregadores, App, Financeiro"
echo ""
docker-compose up

echo ""
echo "=========================================="
echo "  🍕 Pizzaria encerrada"
echo "=========================================="

