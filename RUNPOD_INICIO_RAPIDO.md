# ⚡ RunPod - Inicio Rápido

Guía ultra-rápida para deployar en RunPod en 10 minutos.

## 🎯 Por qué RunPod

- 💰 50-70% más barato que Hugging Face
- ⚡ Cold start en 30 segundos (vs 5 minutos)
- 🔧 Más control y flexibilidad
- 📊 Mejor para alto volumen

## 🚀 Deployment Rápido (Opción 1: Docker)

### 1. Preparar

```bash
# Clonar repo
git clone https://github.com/TU_USUARIO/TU_REPO.git
cd TU_REPO

# Dar permisos al script
chmod +x deploy_runpod.sh
```

### 2. Deployar

```bash
# Ejecutar script automatizado
./deploy_runpod.sh
```

El script te guiará paso a paso:
1. Construye la imagen Docker
2. Te permite probar localmente
3. Sube a Docker Hub
4. Te da las instrucciones para RunPod

### 3. Crear Endpoint en RunPod

1. Ve a https://www.runpod.io/console/serverless
2. Click "New Endpoint"
3. Configuración:
   - **Container Image**: `TU_USUARIO/chatterbox-tts-es:latest`
   - **Container Disk**: 20 GB
   - **GPU**: RTX 4090 (~$0.40/hora)
   - **Max Workers**: 3
   - **Idle Timeout**: 5 segundos

4. Click "Deploy"

### 4. Usar

```python
from runpod_client import ChatterboxRunPodClient

cliente = ChatterboxRunPodClient(
    endpoint_id="tu_endpoint_id",
    api_key="tu_api_key"
)

cliente.generar("Hola, ¿cómo estás?")
```

## 🚀 Deployment Rápido (Opción 2: GitHub)

### 1. Subir a GitHub

```bash
git add .
git commit -m "Preparar para RunPod"
git push
```

### 2. Crear Template en RunPod

1. Ve a https://www.runpod.io/console/serverless
2. Click "Templates" → "New Template"
3. Configuración:
   - **Container Image**: `runpod/pytorch:2.1.0-py3.10-cuda11.8.0-devel`
   - **Container Disk**: 20 GB
   - **Docker Command**:
     ```bash
     bash -c "git clone https://github.com/TU_USUARIO/TU_REPO.git /app && cd /app && pip install -r requirements.txt && pip install runpod && python runpod_handler.py"
     ```

### 3. Crear Endpoint

1. Click "New Endpoint"
2. Selecciona tu template
3. GPU: RTX 4090
4. Deploy

## 💻 Uso Básico

```python
import requests
import base64

response = requests.post(
    "https://api.runpod.ai/v2/TU_ENDPOINT_ID/runsync",
    headers={"Authorization": "Bearer TU_API_KEY"},
    json={
        "input": {
            "texto": "Hola, bienvenido"
        }
    }
)

# Guardar audio
audio = base64.b64decode(response.json()["output"]["audio"])
with open("voz.wav", "wb") as f:
    f.write(audio)
```

## 🧪 Testing Local

```bash
# Con Docker Compose
docker-compose up

# O con Docker directo
docker build -t chatterbox-test .
docker run --gpus all \
    -e RUNPOD_WEBHOOK_GET_JOB='{"input":{"texto":"Prueba"}}' \
    chatterbox-test
```

## 💰 Costos

| GPU | $/hora | Recomendado |
|-----|--------|-------------|
| RTX 4090 | $0.40 | ✅ Mejor relación precio/rendimiento |
| RTX A4000 | $0.50 | Producción |
| RTX A5000 | $0.80 | Alto volumen |

**Con auto-scaling**: Solo pagas cuando se usa (Idle Timeout: 5s)

## 📊 Comparación

| Característica | RunPod | Hugging Face |
|----------------|--------|--------------|
| Costo/hora | $0.40-0.80 | $1.30-4.50 |
| Cold start | ~30s | ~5min |
| Control | Alto | Medio |
| Setup | 10min | 15min |

## 🎯 Personalización

```python
# Voz neutral
cliente.generar(texto="...", expresividad=0.4)

# Voz natural (default)
cliente.generar(texto="...")

# Voz expresiva
cliente.generar(texto="...", expresividad=1.0)
```

## 🐛 Problemas Comunes

### "Container failed to start"
```bash
# Verificar que la imagen se construyó bien
docker build -t test .
docker run --gpus all test
```

### "Out of memory"
→ Aumenta Container Disk a 30 GB en RunPod

### "Endpoint not responding"
→ Verifica que el endpoint esté en estado "Running"

## 📚 Archivos Importantes

- `Dockerfile` - Configuración del contenedor
- `runpod_handler.py` - Handler principal
- `runpod_client.py` - Cliente Python
- `deploy_runpod.sh` - Script de deployment
- `RUNPOD_DEPLOYMENT.md` - Guía completa

## 🎉 ¡Listo!

En 10 minutos tienes un endpoint de síntesis de voz en español funcionando en RunPod, más barato y rápido que otras opciones.

---

**Siguiente paso**: Ejecuta `./deploy_runpod.sh` y sigue las instrucciones.
