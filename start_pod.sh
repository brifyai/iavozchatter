#!/bin/bash
set -e

echo "🚀 Iniciando Chatterbox TTS en RunPod Pod..."

# Actualizar sistema
echo "📦 Instalando dependencias del sistema..."
apt-get update -qq
apt-get install -y -qq git git-lfs libsndfile1 ffmpeg curl

# Clonar repositorio si no existe
if [ ! -d "/workspace/app" ]; then
    echo "📥 Clonando repositorio..."
    git clone https://github.com/brifyai/iavozchatter.git /workspace/app
fi

cd /workspace/app

# Actualizar repo
echo "🔄 Actualizando código..."
git pull

# Instalar dependencias Python
echo "🐍 Instalando dependencias Python..."
pip install --no-cache-dir -q -r requirements.txt

# Iniciar servidor API
echo "🎙️ Iniciando servidor API en puerto 8000..."
python api_server.py
