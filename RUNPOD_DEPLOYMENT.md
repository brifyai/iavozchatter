# 🚀 Deployment en RunPod

Guía completa para deployar Chatterbox TTS en español en RunPod.

## 🎯 Ventajas de RunPod

- 💰 Más económico que Hugging Face (~$0.40-0.80/hora)
- ⚡ Más rápido (cold start ~30s vs 5min)
- 🔧 Más control y flexibilidad
- 📊 Mejor para alto volumen

## 📋 Pre-requisitos

1. Cuenta en [RunPod](https://www.runpod.io/)
2. Créditos en tu cuenta RunPod
3. Repositorio en GitHub con el código

## 🔧 Opción 1: Deployment con Docker (Recomendado)

### Paso 1: Preparar el Repositorio

Asegúrate de tener estos archivos:
```
├── Dockerfile
├── runpod_handler.py
├── requirements.txt
├── src/
│   └── chatterbox/
└── (archivos del modelo se descargan automáticamente)
```

### Paso 2: Construir la Imagen Docker

```bash
# Clonar tu repositorio
git clone https://github.com/TU_USUARIO/TU_REPO.git
cd TU_REPO

# Construir imagen
docker build -t chatterbox-tts-es:latest .

# Probar localmente (opcional)
docker run --gpus all -p 8000:8000 chatterbox-tts-es:latest
```

### Paso 3: Subir a Docker Hub

```bash
# Login a Docker Hub
docker login

# Tag de la imagen
docker tag chatterbox-tts-es:latest TU_USUARIO/chatterbox-tts-es:latest

# Push
docker push TU_USUARIO/chatterbox-tts-es:latest
```

### Paso 4: Crear Endpoint en RunPod

1. Ve a https://www.runpod.io/console/serverless
2. Click en "New Endpoint"
3. Configuración:
   - **Name**: chatterbox-tts-español
   - **Container Image**: `TU_USUARIO/chatterbox-tts-es:latest`
   - **Container Disk**: 20 GB
   - **GPU Type**: RTX 4090 o A4000 (más económico)
   - **Max Workers**: 3
   - **Idle Timeout**: 5 segundos
   - **Execution Timeout**: 60 segundos

4. Click "Deploy"

### Paso 5: Obtener el Endpoint URL

Copia el endpoint URL que aparece, algo como:
```
https://api.runpod.ai/v2/YOUR_ENDPOINT_ID/runsync
```

## 🔧 Opción 2: Deployment desde GitHub (Más Simple)

### Paso 1: Preparar GitHub

Sube todos los archivos a tu repositorio de GitHub:
```bash
git add Dockerfile runpod_handler.py requirements.txt src/
git commit -m "Preparar para RunPod"
git push
```

### Paso 2: Crear Template en RunPod

1. Ve a https://www.runpod.io/console/serverless
2. Click en "Templates" → "New Template"
3. Configuración:
   - **Template Name**: Chatterbox TTS Español
   - **Container Image**: `runpod/pytorch:2.1.0-py3.10-cuda11.8.0-devel`
   - **Container Disk**: 20 GB
   - **Docker Command**: 
     ```bash
     bash -c "cd /workspace && git clone https://github.com/TU_USUARIO/TU_REPO.git && cd TU_REPO && pip install -r requirements.txt && pip install runpod && python runpod_handler.py"
     ```
   - **Environment Variables**:
     - `HF_TOKEN`: tu_token_de_huggingface (si es repo privado)

4. Guardar template

### Paso 3: Crear Endpoint

1. Click en "New Endpoint"
2. Selecciona el template que creaste
3. Configuración:
   - **GPU Type**: RTX 4090 o A4000
   - **Max Workers**: 3
   - **Idle Timeout**: 5 segundos

4. Deploy

## 💻 Uso del Endpoint

### Python

```python
import requests
import base64

RUNPOD_ENDPOINT = "https://api.runpod.ai/v2/YOUR_ENDPOINT_ID/runsync"
RUNPOD_API_KEY = "tu_api_key_de_runpod"

def generar_voz(texto, expresividad=0.6):
    response = requests.post(
        RUNPOD_ENDPOINT,
        headers={
            "Authorization": f"Bearer {RUNPOD_API_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "input": {
                "texto": texto,
                "exaggeration": expresividad,
                "temperature": 0.85
            }
        }
    )
    
    result = response.json()
    
    if "error" in result:
        print(f"❌ Error: {result['error']}")
        return None
    
    # Extraer audio
    audio_base64 = result["output"]["audio"]
    audio_data = base64.b64decode(audio_base64)
    
    # Guardar
    with open("voz.wav", "wb") as f:
        f.write(audio_data)
    
    print("✅ Audio generado: voz.wav")
    return audio_data

# Uso
generar_voz("Hola, bienvenido al sistema de síntesis de voz.")
```

### Cliente Optimizado para RunPod

```python
import requests
import base64
import os

class ChatterboxRunPodClient:
    def __init__(self, endpoint_url, api_key):
        self.endpoint_url = endpoint_url
        self.api_key = api_key
    
    def generar(self, texto, expresividad=0.6, temperatura=0.85, archivo_salida="voz.wav"):
        response = requests.post(
            self.endpoint_url,
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            },
            json={
                "input": {
                    "texto": texto,
                    "exaggeration": expresividad,
                    "temperature": temperatura
                }
            },
            timeout=60
        )
        
        result = response.json()
        
        if "error" in result:
            print(f"❌ Error: {result['error']}")
            return None
        
        # Decodificar audio
        audio_base64 = result["output"]["audio"]
        audio_data = base64.b64decode(audio_base64)
        
        # Guardar
        with open(archivo_salida, "wb") as f:
            f.write(audio_data)
        
        print(f"✅ Audio generado: {archivo_salida}")
        return result["output"]

# Uso
cliente = ChatterboxRunPodClient(
    endpoint_url="https://api.runpod.ai/v2/YOUR_ENDPOINT_ID/runsync",
    api_key="tu_api_key"
)

cliente.generar("Hola, ¿cómo estás?")
```

## 📊 Comparación de Costos

### RunPod
| GPU | Costo/hora | Recomendado para |
|-----|-----------|------------------|
| RTX 4090 | ~$0.40 | Desarrollo, bajo volumen |
| RTX A4000 | ~$0.50 | Producción, medio volumen |
| RTX A5000 | ~$0.80 | Alto volumen |

### Hugging Face
| GPU | Costo/hora |
|-----|-----------|
| A10G | ~$1.30 |
| A100 | ~$4.50 |

**Ahorro**: 50-70% con RunPod

## ⚡ Optimización de Costos

### 1. Idle Timeout Corto
```
Idle Timeout: 5 segundos
```
El worker se apaga cuando no hay requests.

### 2. Auto-scaling
```
Min Workers: 0
Max Workers: 3
```
Escala automáticamente según demanda.

### 3. Usar GPU Económica
```
RTX 4090: Excelente relación precio/rendimiento
```

## 🧪 Testing

### Test Local con Docker

```bash
# Construir
docker build -t chatterbox-test .

# Ejecutar
docker run --gpus all -e RUNPOD_WEBHOOK_GET_JOB='{"input":{"texto":"Hola mundo"}}' chatterbox-test
```

### Test del Endpoint

```python
import requests

response = requests.post(
    "https://api.runpod.ai/v2/YOUR_ENDPOINT_ID/runsync",
    headers={"Authorization": "Bearer YOUR_API_KEY"},
    json={
        "input": {
            "texto": "Prueba de conexión"
        }
    }
)

print(response.json())
```

## 🐛 Troubleshooting

### Error: "Container failed to start"
→ Verifica que el Dockerfile sea correcto y la imagen se construyó bien

### Error: "Out of memory"
→ Aumenta el Container Disk a 30 GB

### Error: "Model not found"
→ Asegúrate de que los archivos del modelo se descarguen correctamente

### Latencia alta
→ Usa una GPU más potente o aumenta Max Workers

## 📊 Monitoreo

RunPod proporciona métricas en tiempo real:
- Requests por minuto
- Latencia promedio
- Tasa de error
- Uso de GPU
- Costos acumulados

Accede en: https://www.runpod.io/console/serverless

## 🔐 Seguridad

1. **API Key**: Guarda tu API key de forma segura
2. **Rate Limiting**: Configura límites en RunPod
3. **Logs**: Revisa logs regularmente
4. **Alertas**: Configura alertas de costos

## 📚 Recursos

- [Documentación RunPod](https://docs.runpod.io/)
- [RunPod Discord](https://discord.gg/runpod)
- [Ejemplos RunPod](https://github.com/runpod/runpod-python)

## 🎉 Ventajas del Setup

✅ Deployment en minutos  
✅ 50-70% más económico  
✅ Auto-scaling automático  
✅ Cold start rápido (~30s)  
✅ Fácil de actualizar  
✅ Métricas en tiempo real  

---

**Siguiente paso**: Ejecuta el deployment y prueba con el cliente de ejemplo.
