#!/bin/bash

# Script de deployment automatizado para RunPod
# Uso: ./deploy_runpod.sh

set -e

echo "🚀 Deployment de Chatterbox TTS en RunPod"
echo "=========================================="

# Colores
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Verificar Docker
if ! command -v docker &> /dev/null; then
    echo -e "${RED}❌ Docker no está instalado${NC}"
    echo "Instala Docker desde: https://docs.docker.com/get-docker/"
    exit 1
fi

echo -e "${GREEN}✅ Docker encontrado${NC}"

# Solicitar información
echo ""
read -p "Docker Hub username: " DOCKER_USER
read -p "Nombre de la imagen (default: chatterbox-tts-es): " IMAGE_NAME
IMAGE_NAME=${IMAGE_NAME:-chatterbox-tts-es}

echo ""
echo "📦 Construyendo imagen Docker..."
docker build -t ${IMAGE_NAME}:latest .

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Imagen construida exitosamente${NC}"
else
    echo -e "${RED}❌ Error al construir la imagen${NC}"
    exit 1
fi

# Preguntar si quiere probar localmente
echo ""
read -p "¿Quieres probar la imagen localmente? (y/n): " TEST_LOCAL

if [ "$TEST_LOCAL" = "y" ] || [ "$TEST_LOCAL" = "Y" ]; then
    echo ""
    echo "🧪 Probando imagen localmente..."
    echo "Presiona Ctrl+C para detener cuando termine la prueba"
    
    docker run --rm --gpus all \
        -e RUNPOD_WEBHOOK_GET_JOB='{"input":{"texto":"Hola, esta es una prueba local"}}' \
        ${IMAGE_NAME}:latest
    
    echo -e "${GREEN}✅ Prueba local completada${NC}"
fi

# Subir a Docker Hub
echo ""
read -p "¿Quieres subir la imagen a Docker Hub? (y/n): " PUSH_IMAGE

if [ "$PUSH_IMAGE" = "y" ] || [ "$PUSH_IMAGE" = "Y" ]; then
    echo ""
    echo "🔐 Iniciando sesión en Docker Hub..."
    docker login
    
    echo ""
    echo "📤 Subiendo imagen a Docker Hub..."
    docker tag ${IMAGE_NAME}:latest ${DOCKER_USER}/${IMAGE_NAME}:latest
    docker push ${DOCKER_USER}/${IMAGE_NAME}:latest
    
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✅ Imagen subida exitosamente${NC}"
        echo ""
        echo "📋 Información para RunPod:"
        echo "   Container Image: ${DOCKER_USER}/${IMAGE_NAME}:latest"
        echo ""
        echo "🔗 Siguiente paso:"
        echo "   1. Ve a https://www.runpod.io/console/serverless"
        echo "   2. Click en 'New Endpoint'"
        echo "   3. Usa la imagen: ${DOCKER_USER}/${IMAGE_NAME}:latest"
        echo "   4. Configura GPU: RTX 4090 o A4000"
        echo "   5. Container Disk: 20 GB"
        echo "   6. Deploy!"
    else
        echo -e "${RED}❌ Error al subir la imagen${NC}"
        exit 1
    fi
fi

echo ""
echo -e "${GREEN}🎉 Deployment completado${NC}"
echo ""
echo "📚 Documentación:"
echo "   - RUNPOD_DEPLOYMENT.md - Guía completa"
echo "   - runpod_client.py - Cliente de ejemplo"
