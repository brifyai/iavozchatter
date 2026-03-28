#!/bin/bash

# Script para construir y subir imagen a Docker Hub
# Uso: ./build_and_push.sh [docker_username]

set -e

DOCKER_USER=${1:-"brifyai"}
IMAGE_NAME="chatterbox-tts-es"
VERSION="latest"

echo "🐳 Construyendo imagen Docker..."
docker build -t ${IMAGE_NAME}:${VERSION} .

echo "✅ Imagen construida"

echo "🏷️  Taggeando imagen..."
docker tag ${IMAGE_NAME}:${VERSION} ${DOCKER_USER}/${IMAGE_NAME}:${VERSION}

echo "🔐 Haciendo login en Docker Hub..."
docker login

echo "📤 Subiendo imagen a Docker Hub..."
docker push ${DOCKER_USER}/${IMAGE_NAME}:${VERSION}

echo ""
echo "✅ ¡Imagen subida exitosamente!"
echo ""
echo "📋 Usa esta imagen en RunPod:"
echo "   ${DOCKER_USER}/${IMAGE_NAME}:${VERSION}"
echo ""
echo "🔧 Configuración para RunPod:"
echo "   Container Image: ${DOCKER_USER}/${IMAGE_NAME}:${VERSION}"
echo "   Container Disk: 20 GB"
echo "   GPU: RTX 4090"
echo "   Docker Command: (dejar vacío)"
