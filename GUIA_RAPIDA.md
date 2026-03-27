# 🚀 Guía Rápida - Chatterbox TTS en Español

## ¿Qué es esto?

Un sistema de síntesis de voz (text-to-speech) en español de alta calidad que puedes usar vía API. Convierte cualquier texto en audio con voz natural y humana.

## 📦 Lo que tienes

Ya está todo listo para deployar:
- ✅ `handler.py` - El código que procesa las solicitudes
- ✅ `requirements.txt` - Las dependencias necesarias
- ✅ Documentación completa
- ✅ Ejemplos de código

## 🎯 Deployment en 3 pasos

### 1. Sube los archivos a Hugging Face

```bash
cd Chatterbox-Multilingual-TTS
git add handler.py requirements.txt
git commit -m "Agregar handler para español"
git push
```

### 2. Crea el endpoint

Ve a https://ui.endpoints.huggingface.co/

- Click en "New Endpoint"
- Selecciona tu repositorio
- Elige GPU [medium] - A10G (mínimo)
- Click "Create Endpoint"

### 3. Espera 5-10 minutos

El sistema se está preparando. Cuando veas "running", ¡está listo!

## 💻 Cómo usarlo

### Ejemplo básico en Python

```python
import requests
import base64

ENDPOINT_URL = "https://tu-endpoint.endpoints.huggingface.cloud"
TOKEN = "tu_token_de_huggingface"

# Hacer la solicitud
response = requests.post(
    ENDPOINT_URL,
    headers={"Authorization": f"Bearer {TOKEN}"},
    json={
        "inputs": "Hola, bienvenido al sistema de síntesis de voz."
    }
)

# Guardar el audio
audio_data = base64.b64decode(response.json()["audio"])
with open("voz.wav", "wb") as f:
    f.write(audio_data)

print("✅ Audio generado: voz.wav")
```

### Con el cliente incluido

```python
from example_client import ChatterboxTTSClient

cliente = ChatterboxTTSClient(ENDPOINT_URL, TOKEN)

# Generar voz
cliente.generar(
    texto="Este es un mensaje de prueba.",
    archivo_salida="mi_audio.wav"
)
```

## 🎨 Personalización

Puedes ajustar cómo suena la voz:

```python
cliente.generar(
    texto="¡Esto es increíble!",
    expresividad=1.0,      # 0.25-2.0 (más alto = más expresivo)
    temperatura=0.9,       # 0.05-5.0 (más alto = más variado)
    archivo_salida="expresivo.wav"
)
```

### Guía de expresividad

- **0.3-0.4**: Voz neutral, profesional (ideal para noticias, informes)
- **0.5-0.7**: Voz natural, conversacional (ideal para asistentes, tutoriales)
- **0.8-1.2**: Voz expresiva, emotiva (ideal para narraciones, publicidad)

## 🎤 Clonar una voz

Si tienes un audio de referencia (3-10 segundos):

```python
cliente.generar(
    texto="Este audio sonará como la voz de referencia.",
    audio_referencia="mi_voz.wav",
    archivo_salida="voz_clonada.wav"
)
```

## 📊 Formato de la solicitud

```json
{
  "inputs": "Tu texto aquí (máximo 300 caracteres)",
  "parameters": {
    "exaggeration": 0.6,
    "temperature": 0.85,
    "cfg_weight": 0.5,
    "seed": 0,
    "audio_prompt_base64": "opcional_audio_en_base64"
  }
}
```

## 📊 Formato de la respuesta

```json
{
  "audio": "UklGRiQAAABXQVZFZm10...",
  "sample_rate": 24000,
  "text": "Tu texto aquí"
}
```

El audio viene en formato WAV codificado en base64.

## 🧪 Probar localmente

Antes de deployar, puedes probar:

```bash
python test_handler.py
```

## 💰 Costos aproximados

- GPU A10G: ~$1.30/hora
- GPU A100: ~$4.50/hora

Tip: Usa auto-scaling para pagar solo cuando se use.

## ❓ Problemas comunes

### "No handler.py file was found"
→ Asegúrate de que `handler.py` está en la raíz del repositorio

### "Module not found"
→ Verifica que `requirements.txt` tiene todas las dependencias

### El audio suena robótico
→ Aumenta la `expresividad` a 0.7-0.9

### El audio es muy lento/rápido
→ Ajusta `cfg_weight` (0.3 = más rápido, 0.7 = más lento)

## 📚 Más información

- `example_client.py` - Cliente completo con ejemplos
- `DEPLOYMENT.md` - Guía detallada de deployment
- `test_handler.py` - Pruebas locales

## 🎉 ¡Listo!

Con esto ya puedes convertir texto a voz en español de forma profesional. El sistema genera audio de 24kHz con calidad de estudio.

---

**Características principales:**
- ✅ Voz natural y humana en español
- ✅ Control de expresividad y estilo
- ✅ Clonación de voz desde audio de referencia
- ✅ API REST lista para producción
- ✅ Audio de alta calidad (24kHz)
