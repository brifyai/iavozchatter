# 🚀 Guía de Deployment en Hugging Face Inference Endpoints

Esta guía te ayudará a deployar el modelo Chatterbox Multilingual TTS en Hugging Face Inference Endpoints.

## 📋 Pre-requisitos

1. Cuenta de Hugging Face con acceso a Inference Endpoints
2. Token de acceso de Hugging Face con permisos de escritura
3. Repositorio del modelo en Hugging Face Hub

## 🔧 Archivos Necesarios

El repositorio debe contener estos archivos para el deployment:

```
├── handler.py                 # ✅ Handler personalizado (REQUERIDO)
├── requirements.txt           # ✅ Dependencias (REQUERIDO)
├── src/                       # ✅ Código fuente del modelo
│   └── chatterbox/
├── ve.pt                      # ✅ Pesos del Voice Encoder
├── t3_mtl23ls_v2.safetensors # ✅ Pesos del modelo T3
├── s3gen.pt                   # ✅ Pesos del generador S3
├── grapheme_mtl_merged_expanded_v1.json  # ✅ Tokenizer
├── conds.pt                   # ✅ Condiciones por defecto
└── Cangjie5_TC.json          # ✅ Para soporte de chino
```

## 📝 Pasos para Deployment

### 1. Preparar el Repositorio

Asegúrate de que todos los archivos necesarios estén en tu repositorio de Hugging Face:

```bash
# Clonar tu repositorio
git clone https://huggingface.co/YOUR_USERNAME/YOUR_MODEL_NAME
cd YOUR_MODEL_NAME

# Copiar los archivos necesarios
cp handler.py YOUR_MODEL_NAME/
cp requirements.txt YOUR_MODEL_NAME/
cp -r src/ YOUR_MODEL_NAME/

# Commit y push
git add .
git commit -m "Add custom handler for Inference Endpoints"
git push
```

### 2. Verificar handler.py

El archivo `handler.py` debe estar en la raíz del repositorio y contener la clase `EndpointHandler` con los métodos `__init__` y `__call__`.

### 3. Crear el Endpoint

#### Opción A: Desde la UI de Hugging Face

1. Ve a https://ui.endpoints.huggingface.co/
2. Click en "New Endpoint"
3. Selecciona tu repositorio del modelo
4. Configura las opciones:
   - **Task**: Se detectará automáticamente como "Custom"
   - **Cloud Provider**: AWS, Azure, o GCP
   - **Region**: Selecciona la más cercana a tus usuarios
   - **Instance Type**: 
     - Mínimo recomendado: `GPU [medium] - 1x Nvidia A10G`
     - Óptimo: `GPU [xlarge] - 1x Nvidia A100`
   - **Scaling**: 
     - Min replicas: 1
     - Max replicas: según necesidad
5. Click en "Create Endpoint"

#### Opción B: Usando la API

```python
from huggingface_hub import create_inference_endpoint

endpoint = create_inference_endpoint(
    name="chatterbox-multilingual-tts",
    repository="YOUR_USERNAME/YOUR_MODEL_NAME",
    framework="custom",
    task="custom",
    accelerator="gpu",
    instance_size="medium",
    instance_type="nvidia-a10g",
    region="us-east-1",
    vendor="aws",
    min_replica=1,
    max_replica=1,
    token="YOUR_HF_TOKEN"
)

print(f"Endpoint URL: {endpoint.url}")
```

### 4. Monitorear el Deployment

El deployment puede tomar 5-15 minutos. Puedes monitorear el progreso:

1. En la UI: Ve a tu endpoint y revisa los logs
2. Estados posibles:
   - `initializing`: Preparando el contenedor
   - `pending`: Descargando modelo y dependencias
   - `running`: ✅ Endpoint listo para usar
   - `failed`: ❌ Revisa los logs para errores

### 5. Probar el Endpoint

Una vez que el estado sea `running`:

```python
import requests
import base64

ENDPOINT_URL = "https://your-endpoint.endpoints.huggingface.cloud"
HEADERS = {
    "Authorization": "Bearer YOUR_HF_TOKEN",
    "Content-Type": "application/json"
}

# Test básico
payload = {
    "inputs": "Hola, este es un test del endpoint.",
    "parameters": {
        "language_id": "es"
    }
}

response = requests.post(ENDPOINT_URL, headers=HEADERS, json=payload)
print(response.json())
```

## 🐛 Troubleshooting

### Error: "No handler.py file was found"

**Solución**: Asegúrate de que `handler.py` está en la raíz del repositorio.

```bash
# Verificar estructura
ls -la
# Debe mostrar handler.py en la raíz
```

### Error: "Module not found"

**Solución**: Verifica que todas las dependencias estén en `requirements.txt`:

```txt
gradio
numpy>=1.26.2
resampy==0.4.3
librosa==0.10.0
s3tokenizer
transformers==4.46.3
diffusers==0.29.0
omegaconf==2.3.0
resemble-perth==1.0.1
silero-vad==5.1.2
conformer==0.3.2
safetensors
soundfile
```

### Error: "CUDA out of memory"

**Solución**: Aumenta el tamaño de la instancia GPU:
- De `medium` a `xlarge`
- O reduce el batch size en el handler

### Error: "Model files not found"

**Solución**: Asegúrate de que todos los archivos del modelo estén en el repositorio:

```bash
# Verificar archivos del modelo
ls -la *.pt *.safetensors *.json
```

### Endpoint muy lento

**Soluciones**:
1. Aumentar el tamaño de la instancia
2. Habilitar auto-scaling (aumentar max_replica)
3. Usar una región más cercana a tus usuarios
4. Implementar caching en tu aplicación

## 💰 Costos Estimados

Los costos varían según el proveedor y región. Ejemplo en AWS:

| Instance Type | GPU | Costo/hora (aprox) |
|---------------|-----|-------------------|
| GPU [small] | T4 | $0.60 |
| GPU [medium] | A10G | $1.30 |
| GPU [xlarge] | A100 | $4.50 |

**Tip**: Usa auto-scaling para reducir costos cuando no hay tráfico.

## 🔒 Seguridad

### Proteger tu Endpoint

1. **Usar tokens de acceso**: Siempre requiere autenticación
2. **Rate limiting**: Configura límites de requests
3. **Monitoring**: Activa alertas para uso anormal
4. **Validación de inputs**: El handler ya incluye validación básica

### Variables de Entorno

Si necesitas configurar variables de entorno (como `HF_TOKEN`):

```python
# En la UI de Hugging Face
# Settings > Environment Variables
HF_TOKEN=your_token_here
```

## 📊 Monitoreo y Logs

### Ver Logs en Tiempo Real

```python
from huggingface_hub import get_inference_endpoint

endpoint = get_inference_endpoint("chatterbox-multilingual-tts", token="YOUR_HF_TOKEN")
logs = endpoint.get_logs()
print(logs)
```

### Métricas Importantes

- **Latencia**: Tiempo de respuesta promedio
- **Throughput**: Requests por segundo
- **Error rate**: Porcentaje de requests fallidos
- **GPU utilization**: Uso de GPU (debe estar > 70% para eficiencia)

## 🔄 Actualizar el Endpoint

Para actualizar el modelo o handler:

```bash
# 1. Hacer cambios en tu repositorio local
git add .
git commit -m "Update handler"
git push

# 2. Reiniciar el endpoint
# Opción A: Desde la UI (botón "Restart")
# Opción B: Usando la API
```

```python
from huggingface_hub import get_inference_endpoint

endpoint = get_inference_endpoint("chatterbox-multilingual-tts", token="YOUR_HF_TOKEN")
endpoint.pause()  # Pausar
endpoint.resume()  # Reanudar (cargará la nueva versión)
```

## 📚 Recursos Adicionales

- [Documentación oficial de Inference Endpoints](https://huggingface.co/docs/inference-endpoints)
- [Pricing de Inference Endpoints](https://huggingface.co/pricing#endpoints)
- [Ejemplos de Custom Handlers](https://huggingface.co/models?other=endpoints-template)
- [ENDPOINT_USAGE.md](./ENDPOINT_USAGE.md) - Guía de uso del endpoint

## ✅ Checklist de Deployment

- [ ] `handler.py` en la raíz del repositorio
- [ ] `requirements.txt` con todas las dependencias
- [ ] Todos los archivos del modelo (.pt, .safetensors, .json) en el repo
- [ ] Código fuente (`src/chatterbox/`) incluido
- [ ] Token de Hugging Face con permisos correctos
- [ ] Endpoint creado y en estado `running`
- [ ] Test básico exitoso
- [ ] Documentación de uso compartida con el equipo
- [ ] Monitoreo y alertas configurados

## 🎉 ¡Listo!

Tu modelo Chatterbox Multilingual TTS ahora está deployado y listo para ser consumido vía API. Consulta [ENDPOINT_USAGE.md](./ENDPOINT_USAGE.md) para ejemplos de uso.
