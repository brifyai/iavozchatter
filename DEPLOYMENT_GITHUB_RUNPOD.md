# 🚀 Deployment desde GitHub en RunPod

Guía para deployar directamente desde tu repositorio de GitHub en RunPod.

## 📋 Información del Repositorio

- **Repositorio**: https://github.com/brifyai/iavozchatter.git
- **Branch**: main
- **Configurado con**: brifyaimaster@gmail.com

## ⚡ Deployment Rápido (Opción Recomendada)

### Paso 1: Crear Template en RunPod

1. Ve a https://www.runpod.io/console/serverless
2. Click en **"Templates"** → **"New Template"**
3. Configuración:

```
Template Name: Chatterbox TTS Español
Container Image: runpod/pytorch:2.1.0-py3.10-cuda11.8.0-devel-ubuntu22.04
Container Disk: 20 GB

Docker Command:
bash -c "apt-get update && apt-get install -y git git-lfs libsndfile1 ffmpeg && git clone https://github.com/brifyai/iavozchatter.git /app && cd /app && pip install --no-cache-dir -r requirements.txt && pip install --no-cache-dir runpod && python -u runpod_handler.py"

Environment Variables:
(opcional) HF_TOKEN=tu_token_si_necesitas
```

4. Click **"Save Template"**

### Paso 2: Crear Endpoint

1. Click en **"New Endpoint"**
2. Selecciona el template que acabas de crear
3. Configuración del Endpoint:

```
Endpoint Name: chatterbox-tts-español
GPU Type: RTX 4090 (recomendado - $0.40/hora)
Min Workers: 0
Max Workers: 3
Idle Timeout: 5 segundos
Execution Timeout: 60 segundos
```

4. Click **"Deploy"**

### Paso 3: Esperar

- El deployment toma ~2-3 minutos
- Verás el estado cambiar a "Running"
- Copia el **Endpoint ID** que aparece

### Paso 4: Obtener API Key

1. Ve a **Settings** en RunPod
2. Copia tu **API Key**

### Paso 5: Probar

```python
from runpod_client import ChatterboxRunPodClient

cliente = ChatterboxRunPodClient(
    endpoint_id="TU_ENDPOINT_ID",  # Del paso 3
    api_key="TU_API_KEY"            # Del paso 4
)

# Generar voz
cliente.generar(
    texto="Hola, bienvenido al sistema de síntesis de voz en español.",
    archivo_salida="prueba.wav"
)
```

## 🔧 Configuración Detallada

### Docker Command Explicado

```bash
# Actualizar sistema
apt-get update && apt-get install -y git git-lfs libsndfile1 ffmpeg

# Clonar repositorio
git clone https://github.com/brifyai/iavozchatter.git /app

# Ir al directorio
cd /app

# Instalar dependencias
pip install --no-cache-dir -r requirements.txt
pip install --no-cache-dir runpod

# Ejecutar handler
python -u runpod_handler.py
```

### Variables de Entorno Opcionales

```
HF_TOKEN=tu_token_de_huggingface
```
Solo necesario si el repositorio de Hugging Face es privado.

## 💰 Costos Estimados

### GPU Recomendadas

| GPU | Costo/hora | Uso Recomendado |
|-----|-----------|-----------------|
| RTX 4090 | $0.40 | ✅ Desarrollo y producción |
| RTX A4000 | $0.50 | Producción estable |
| RTX A5000 | $0.80 | Alto volumen |

### Ejemplo de Costos

**1000 requests/día** (8s por request):
- Tiempo total: 1000 × 8s = 2.2 horas/día
- Costo con RTX 4090: 2.2 × $0.40 = **$0.88/día**
- **Mensual: ~$26**

Con auto-scaling (Idle Timeout: 5s), solo pagas cuando hay requests activos.

## 🧪 Testing del Endpoint

### Test Básico

```python
import requests

response = requests.post(
    "https://api.runpod.ai/v2/TU_ENDPOINT_ID/runsync",
    headers={
        "Authorization": "Bearer TU_API_KEY",
        "Content-Type": "application/json"
    },
    json={
        "input": {
            "texto": "Prueba de conexión"
        }
    }
)

print(response.json())
```

### Health Check

```python
from runpod_client import ChatterboxRunPodClient

cliente = ChatterboxRunPodClient(endpoint_id, api_key)

if cliente.health_check():
    print("✅ Endpoint funcionando correctamente")
else:
    print("❌ Endpoint con problemas")
```

## 🔄 Actualizar el Código

Cuando hagas cambios en el código:

### 1. Push a GitHub

```bash
git add .
git commit -m "Actualización del modelo"
git push
```

### 2. Reiniciar Endpoint en RunPod

1. Ve a tu endpoint en RunPod
2. Click en **"..."** → **"Restart"**
3. El endpoint descargará la última versión automáticamente

## 📊 Monitoreo

### Ver Logs en Tiempo Real

1. Ve a tu endpoint en RunPod
2. Click en **"Logs"**
3. Verás la salida del handler en tiempo real

### Métricas Disponibles

- Requests por minuto
- Latencia promedio
- Tasa de error
- Uso de GPU
- Costos acumulados

## 🐛 Troubleshooting

### Error: "Failed to clone repository"

**Solución**: Verifica que el repositorio sea público o agrega un token de GitHub:

```bash
git clone https://TOKEN@github.com/brifyai/iavozchatter.git /app
```

### Error: "Module not found"

**Solución**: Verifica que `requirements.txt` tenga todas las dependencias:

```bash
# Agregar al Docker Command antes de pip install
pip install --upgrade pip
```

### Error: "Out of memory"

**Solución**: Aumenta Container Disk a 30 GB

### Endpoint muy lento

**Solución**: 
1. Aumenta Max Workers a 5
2. Usa GPU más potente (RTX A5000)

### Cold start lento

**Solución**: El primer request toma ~30-60s mientras descarga el modelo. Requests subsecuentes son rápidos (5-8s).

## 🎯 Optimizaciones

### 1. Pre-descargar Modelo

Modifica el Dockerfile para pre-descargar el modelo:

```dockerfile
# Agregar al final del Dockerfile
RUN python -c "from src.chatterbox.mtl_tts import ChatterboxMultilingualTTS; ChatterboxMultilingualTTS.from_pretrained('cuda')"
```

Luego usa la imagen Docker en lugar del comando git clone.

### 2. Caching Agresivo

```python
# En tu aplicación
from functools import lru_cache

@lru_cache(maxsize=100)
def generar_cached(texto):
    return cliente.generar(texto)
```

### 3. Batch Processing

```python
# Generar múltiples audios de una vez
textos = ["texto1", "texto2", "texto3"]
resultados = cliente.generar_varios(textos)
```

## 📚 Archivos Importantes en el Repo

```
iavozchatter/
├── runpod_handler.py       # Handler principal
├── runpod_client.py        # Cliente Python
├── requirements.txt        # Dependencias
├── src/chatterbox/         # Código del modelo
├── Dockerfile              # Para build personalizado
└── RUNPOD_*.md            # Documentación
```

## 🎉 Ventajas de este Setup

✅ **Deployment automático desde GitHub**
- Push código → Restart endpoint → Actualizado

✅ **Sin Docker Hub necesario**
- Todo desde GitHub directamente

✅ **Fácil de mantener**
- Un solo repositorio para todo

✅ **Económico**
- $0.40/hora con RTX 4090
- Auto-scaling incluido

✅ **Rápido**
- Cold start ~30-60s
- Warm requests ~5-8s

## 🔗 Links Útiles

- **Repositorio**: https://github.com/brifyai/iavozchatter.git
- **RunPod Console**: https://www.runpod.io/console/serverless
- **Documentación RunPod**: https://docs.runpod.io/

## 📞 Siguiente Paso

1. Crea el template en RunPod con el comando de arriba
2. Crea el endpoint
3. Prueba con `runpod_client.py`
4. ¡Listo para producción!

---

**Tiempo total de setup**: ~5 minutos  
**Costo estimado**: $0.40/hora (RTX 4090)  
**Latencia**: 5-8 segundos por request
