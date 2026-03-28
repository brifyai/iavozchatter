# 🔧 Solución al Problema de Bucle en RunPod

## 🎯 El Problema

El endpoint se reinicia en bucle porque:
1. El script termina en lugar de quedarse ejecutando
2. RunPod no ve logs porque el contenedor falla antes

## ✅ Solución Rápida (Sin Docker Hub)

### Opción 1: Usar Imagen Pre-construida (Recomendado)

Usa esta configuración en RunPod:

```
Container Image: runpod/pytorch:2.1.0-py3.10-cuda11.8.0-devel-ubuntu22.04

Container Disk: 25 GB (aumentado)

Docker Command:
bash -c 'apt-get update -qq && apt-get install -y -qq git git-lfs libsndfile1 ffmpeg && rm -rf /app && git clone https://github.com/brifyai/iavozchatter.git /app && cd /app && pip install --no-cache-dir -q -r requirements.txt && pip install --no-cache-dir -q runpod && exec python -u runpod_handler.py'

Environment Variables:
PYTHONUNBUFFERED=1
```

**Clave**: El `exec` antes de `python` es CRÍTICO.

### Opción 2: Usar Script de Inicio

```
Container Image: runpod/pytorch:2.1.0-py3.10-cuda11.8.0-devel-ubuntu22.04

Container Disk: 25 GB

Docker Command:
bash -c 'curl -fsSL https://raw.githubusercontent.com/brifyai/iavozchatter/main/start_runpod.sh | bash'
```

## 🐛 Si Sigue Sin Funcionar

### Verificar en RunPod Console:

1. **Ve a "Logs"** en tu endpoint
2. Si no hay logs, el problema es la imagen base o el comando
3. Si hay logs pero termina, el problema es el script

### Prueba Local Primero:

```bash
# En tu máquina con Docker
docker run --rm -it --gpus all \
  -e PYTHONUNBUFFERED=1 \
  runpod/pytorch:2.1.0-py3.10-cuda11.8.0-devel-ubuntu22.04 \
  bash -c 'apt-get update && apt-get install -y git libsndfile1 && git clone https://github.com/brifyai/iavozchatter.git /app && cd /app && pip install -r requirements.txt && pip install runpod && python -u runpod_handler.py'
```

Si funciona local, funcionará en RunPod.

## 🚀 Solución Definitiva: Docker Hub

Si las opciones anteriores no funcionan, usa Docker Hub:

### 1. Build Local

```bash
cd Chatterbox-Multilingual-TTS
docker build -t chatterbox-tts-es .
```

### 2. Test Local

```bash
docker run --rm --gpus all \
  -e RUNPOD_WEBHOOK_GET_JOB='{"input":{"texto":"Prueba"}}' \
  chatterbox-tts-es
```

### 3. Push a Docker Hub

```bash
docker tag chatterbox-tts-es TU_USUARIO/chatterbox-tts-es:latest
docker push TU_USUARIO/chatterbox-tts-es:latest
```

### 4. Usar en RunPod

```
Container Image: TU_USUARIO/chatterbox-tts-es:latest
Container Disk: 20 GB
Docker Command: (vacío)
```

## 📊 Configuración Recomendada

```
Template Name: Chatterbox TTS ES
Container Image: runpod/pytorch:2.1.0-py3.10-cuda11.8.0-devel-ubuntu22.04
Container Disk: 25 GB
Volume Disk: 0 GB
Volume Mount Path: (vacío)

Docker Command:
bash -c 'set -e && apt-get update -qq && apt-get install -y -qq git git-lfs libsndfile1 ffmpeg && rm -rf /app && git clone https://github.com/brifyai/iavozchatter.git /app && cd /app && pip install --no-cache-dir -q -r requirements.txt && pip install --no-cache-dir -q runpod && echo "✅ Setup completo" && exec python -u runpod_handler.py'

Environment Variables:
PYTHONUNBUFFERED=1
CUDA_VISIBLE_DEVICES=0

Endpoint Configuration:
GPU Type: RTX 4090
Min Workers: 0
Max Workers: 1
Idle Timeout: 5
Execution Timeout: 60
```

## 🔍 Debug: Ver Qué Está Pasando

Si quieres ver logs detallados, usa este comando temporal:

```bash
bash -c 'set -x && apt-get update && apt-get install -y git libsndfile1 ffmpeg && git clone https://github.com/brifyai/iavozchatter.git /app && cd /app && pip install -r requirements.txt && pip install runpod && python -u runpod_handler.py 2>&1 | tee /tmp/startup.log'
```

El `set -x` mostrará cada comando que se ejecuta.

## ⚡ Solución Ultra-Rápida

Si tienes prisa, usa Hugging Face en lugar de RunPod:

1. Sube `handler.py` a tu repo de HF
2. Crea endpoint en HF
3. Funciona a la primera (aunque más caro)

Ver: `GUIA_RAPIDA.md`

## 📞 Siguiente Paso

1. Copia el Docker Command de "Configuración Recomendada"
2. Pégalo en tu template de RunPod
3. Aumenta Container Disk a 25 GB
4. Redeploy
5. Espera 3-5 minutos
6. Debería funcionar

Si sigue fallando, comparte:
- Screenshot de la configuración del template
- Cualquier mensaje de error que veas
- El estado del endpoint (Initializing, Failed, etc.)
