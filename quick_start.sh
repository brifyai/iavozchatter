#!/bin/bash
# Script de inicio rápido para RunPod Pod
cd /workspace && \
git clone https://github.com/brifyai/iavozchatter.git app 2>/dev/null || (cd app && git pull) && \
cd app && \
pip install -q -r requirements.txt && \
nohup python -u api_server.py > /workspace/tts.log 2>&1 &
echo "✅ Servidor iniciado en background"
echo "📋 Ver logs: tail -f /workspace/tts.log"
echo "🔗 URL: https://TU_POD_ID-8000.proxy.runpod.net/health"
