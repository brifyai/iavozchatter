#!/bin/bash
set -e

echo "🚀 Iniciando deployment de Chatterbox TTS..."

# Actualizar sistema
echo "📦 Instalando dependencias del sistema..."
apt-get update -qq
apt-get install -y -qq git git-lfs libsndfile1 ffmpeg > /dev/null 2>&1

# Clonar repositorio
echo "📥 Clonando repositorio..."
if [ ! -d "/app" ]; then
    git clone https://github.com/brifyai/iavozchatter.git /app
fi

cd /app

# Instalar dependencias Python
echo "🐍 Instalando dependencias Python..."
pip install --no-cache-dir -q -r requirements.txt
pip install --no-cache-dir -q runpod

# Ejecutar handler (esto debe mantenerse ejecutando)
echo "🎙️ Iniciando handler de TTS..."
exec python -u runpod_handler.py
