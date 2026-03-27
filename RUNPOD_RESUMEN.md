# 📦 RunPod - Resumen Completo

## ✅ Archivos Creados para RunPod

### 🔧 Archivos Técnicos
1. **Dockerfile** - Configuración del contenedor Docker
2. **runpod_handler.py** - Handler principal para RunPod Serverless
3. **runpod_client.py** - Cliente Python optimizado para RunPod
4. **docker-compose.yml** - Para testing local con Docker
5. **.dockerignore** - Optimiza el build de Docker
6. **deploy_runpod.sh** - Script de deployment automatizado

### 📚 Documentación
7. **RUNPOD_DEPLOYMENT.md** - Guía completa y detallada
8. **RUNPOD_INICIO_RAPIDO.md** - Guía rápida (10 minutos)
9. **RUNPOD_RESUMEN.md** - Este archivo

## 🎯 Ventajas de RunPod

| Característica | RunPod | Hugging Face |
|----------------|--------|--------------|
| **Costo/hora** | $0.40-0.80 | $1.30-4.50 |
| **Ahorro** | 50-70% | - |
| **Cold start** | ~30 segundos | ~5 minutos |
| **Control** | Alto | Medio |
| **Flexibilidad** | Alta | Media |
| **Setup** | 10 minutos | 15 minutos |
| **Auto-scaling** | Sí | Sí |
| **Métricas** | Tiempo real | Tiempo real |

## 🚀 Dos Formas de Deployar

### Opción 1: Con Docker (Recomendado)

**Ventajas**:
- ✅ Más rápido (cold start ~30s)
- ✅ Más control
- ✅ Fácil de actualizar
- ✅ Testing local simple

**Pasos**:
```bash
# 1. Ejecutar script
./deploy_runpod.sh

# 2. Crear endpoint en RunPod con tu imagen
# Container Image: TU_USUARIO/chatterbox-tts-es:latest
```

### Opción 2: Desde GitHub

**Ventajas**:
- ✅ No necesitas Docker Hub
- ✅ Deployment directo desde GitHub
- ✅ Más simple para principiantes

**Pasos**:
1. Sube código a GitHub
2. Crea template en RunPod con comando de git clone
3. Crea endpoint con el template

## 💻 Uso del Endpoint

### Con el Cliente Incluido

```python
from runpod_client import ChatterboxRunPodClient

cliente = ChatterboxRunPodClient(
    endpoint_id="tu_endpoint_id",
    api_key="tu_api_key"
)

# Generar voz
cliente.generar(
    texto="Hola, bienvenido",
    expresividad=0.6,
    archivo_salida="voz.wav"
)
```

### Con Requests Directo

```python
import requests
import base64

response = requests.post(
    "https://api.runpod.ai/v2/TU_ENDPOINT_ID/runsync",
    headers={"Authorization": "Bearer TU_API_KEY"},
    json={
        "input": {
            "texto": "Hola mundo",
            "exaggeration": 0.6,
            "temperature": 0.85
        }
    }
)

audio = base64.b64decode(response.json()["output"]["audio"])
with open("voz.wav", "wb") as f:
    f.write(audio)
```

## 🧪 Testing Local

### Con Docker Compose

```bash
# Iniciar
docker-compose up

# Detener
docker-compose down
```

### Con Docker Directo

```bash
# Build
docker build -t chatterbox-test .

# Run
docker run --gpus all \
    -e RUNPOD_WEBHOOK_GET_JOB='{"input":{"texto":"Prueba"}}' \
    chatterbox-test
```

## 💰 Optimización de Costos

### 1. Auto-scaling Agresivo
```
Min Workers: 0
Max Workers: 3
Idle Timeout: 5 segundos
```
→ Solo pagas cuando hay requests activos

### 2. GPU Económica
```
RTX 4090: $0.40/hora
```
→ Excelente rendimiento a bajo costo

### 3. Caching en Cliente
```python
# Cachea respuestas comunes
cache = {}
if texto in cache:
    return cache[texto]
```

## 📊 Estimación de Costos

### Ejemplo: 1000 requests/día

**RunPod (RTX 4090)**:
- Latencia promedio: 8 segundos
- Tiempo total: 1000 × 8s = 8000s = 2.2 horas
- Costo: 2.2 × $0.40 = **$0.88/día** = **$26/mes**

**Hugging Face (A10G)**:
- Mismo uso
- Costo: 2.2 × $1.30 = **$2.86/día** = **$86/mes**

**Ahorro**: $60/mes (70%)

## 🔧 Configuración Recomendada

### Para Desarrollo
```
GPU: RTX 4090
Container Disk: 20 GB
Max Workers: 1
Idle Timeout: 5s
```

### Para Producción
```
GPU: RTX 4090 o A4000
Container Disk: 20 GB
Max Workers: 3-5
Idle Timeout: 5s
Execution Timeout: 60s
```

### Para Alto Volumen
```
GPU: RTX A5000
Container Disk: 30 GB
Max Workers: 10
Idle Timeout: 10s
```

## 🐛 Troubleshooting

### Container no inicia
```bash
# Verificar build local
docker build -t test .
docker run --gpus all test
```

### Out of memory
→ Aumenta Container Disk a 30 GB

### Latencia alta
→ Usa GPU más potente o aumenta Max Workers

### Endpoint no responde
→ Verifica estado en RunPod console

## 📚 Documentación por Nivel

### Principiante
1. **RUNPOD_INICIO_RAPIDO.md** - Empieza aquí (10 min)
2. **runpod_client.py** - Código de ejemplo

### Intermedio
1. **RUNPOD_DEPLOYMENT.md** - Guía completa
2. **Dockerfile** - Configuración del contenedor
3. **docker-compose.yml** - Testing local

### Avanzado
1. **runpod_handler.py** - Handler personalizado
2. **deploy_runpod.sh** - Automatización
3. Optimización de costos y rendimiento

## 🎯 Casos de Uso Ideales para RunPod

✅ **Perfecto para**:
- Startups con presupuesto limitado
- Proyectos con tráfico variable
- Desarrollo y testing
- APIs de alto volumen
- Aplicaciones que necesitan baja latencia

❌ **No ideal para**:
- Si ya tienes créditos de Hugging Face
- Si prefieres managed service completo
- Si no quieres gestionar Docker

## 🔄 Actualización del Modelo

### Con Docker
```bash
# 1. Actualizar código
git pull

# 2. Rebuild y push
./deploy_runpod.sh

# 3. Reiniciar endpoint en RunPod
```

### Desde GitHub
```bash
# 1. Push cambios
git push

# 2. Reiniciar endpoint en RunPod
# (descargará la última versión automáticamente)
```

## 🎉 Resumen Ejecutivo

**RunPod es la mejor opción si**:
- Quieres ahorrar 50-70% en costos
- Necesitas cold start rápido (<30s)
- Quieres más control y flexibilidad
- Tienes tráfico variable (auto-scaling)

**Deployment en 3 pasos**:
1. `./deploy_runpod.sh`
2. Crear endpoint en RunPod
3. Usar con `runpod_client.py`

**Costo típico**: $0.40/hora con RTX 4090

---

**Siguiente paso**: Lee [RUNPOD_INICIO_RAPIDO.md](./RUNPOD_INICIO_RAPIDO.md) y ejecuta `./deploy_runpod.sh`
