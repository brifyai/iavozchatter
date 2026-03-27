---
title: Chatterbox-TTS-Español
emoji: 🎙️
colorFrom: indigo
colorTo: blue
sdk: gradio
sdk_version: 5.29.0
app_file: app.py
pinned: false
short_description: Síntesis de voz en español de alta calidad
---

# 🎙️ Chatterbox TTS - Español

Sistema de síntesis de voz (text-to-speech) en español de alta calidad con control de expresividad y clonación de voz.

## 🚀 Inicio Rápido

### Usar el API

```python
import requests
import base64

response = requests.post(
    "https://tu-endpoint.endpoints.huggingface.cloud",
    headers={"Authorization": "Bearer TU_TOKEN"},
    json={"inputs": "Hola, bienvenido al sistema de síntesis de voz."}
)

# Guardar audio
audio = base64.b64decode(response.json()["audio"])
with open("voz.wav", "wb") as f:
    f.write(audio)
```

### Demo Local

```bash
python app.py
```

## ✨ Características

- 🗣️ Voz natural y humana en español
- 🎨 Control de expresividad (neutral a muy expresivo)
- 🎤 Clonación de voz desde audio de referencia
- ⚡ API REST lista para producción
- 🎵 Audio de alta calidad (24kHz)

## 📚 Documentación

- **[GUIA_RAPIDA.md](./GUIA_RAPIDA.md)** - Empieza aquí (5 minutos)
- **[EJEMPLOS_USO.md](./EJEMPLOS_USO.md)** - Casos de uso prácticos
- **[example_client.py](./example_client.py)** - Cliente Python completo
- **[DEPLOYMENT.md](./DEPLOYMENT.md)** - Guía de deployment detallada

## 🎯 Casos de Uso

- Asistentes virtuales
- Narración de noticias
- Contenido educativo
- Audiolibros
- Sistemas IVR
- Videojuegos
- Marketing y publicidad

## 🔧 Instalación

```bash
pip install -r requirements.txt
```

## 💻 Ejemplo de Uso

```python
from example_client import ChatterboxTTSClient

cliente = ChatterboxTTSClient(ENDPOINT_URL, TOKEN)

# Voz natural
cliente.generar(
    texto="Hola, ¿cómo estás?",
    expresividad=0.6,
    archivo_salida="saludo.wav"
)

# Voz expresiva
cliente.generar(
    texto="¡Esto es increíble!",
    expresividad=1.0,
    archivo_salida="emocionado.wav"
)
```

## 🎨 Control de Expresividad

- **0.3-0.4**: Neutral, profesional
- **0.5-0.7**: Natural, conversacional
- **0.8-1.2**: Expresivo, emotivo

## 📦 Archivos Incluidos

- `handler.py` - Handler para Hugging Face Endpoints
- `example_client.py` - Cliente Python con ejemplos
- `test_handler.py` - Pruebas locales
- Documentación completa en español

## 🚀 Deployment

### Opción 1: RunPod (Recomendado - Más Económico)

```bash
# Deployment automatizado
./deploy_runpod.sh
```

- 💰 50-70% más barato ($0.40/hora vs $1.30/hora)
- ⚡ Cold start en 30 segundos
- 🔧 Más control y flexibilidad

Ver [RUNPOD_INICIO_RAPIDO.md](./RUNPOD_INICIO_RAPIDO.md) para guía completa.

### Opción 2: Hugging Face Inference Endpoints

1. Sube los archivos a tu repositorio de Hugging Face
2. Crea un Inference Endpoint (GPU A10G mínimo)
3. ¡Listo! Usa el API

Ver [GUIA_RAPIDA.md](./GUIA_RAPIDA.md) para instrucciones detalladas.

## 💰 Costos

### RunPod (Recomendado)
- RTX 4090: ~$0.40/hora
- RTX A4000: ~$0.50/hora
- RTX A5000: ~$0.80/hora

### Hugging Face
- GPU A10G: ~$1.30/hora
- GPU A100: ~$4.50/hora

**Ahorro con RunPod**: 50-70%

Usa auto-scaling para optimizar costos.

## 🏢 Uso Comercial

Para versión hosted y fine-tuning, visita [resemble.ai](https://app.resemble.ai)

---

**Calidad de audio**: 24kHz WAV  
**Latencia típica**: 5-10 segundos  
**Longitud máxima**: 300 caracteres por solicitud