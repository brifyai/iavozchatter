# Chatterbox Multilingual TTS - Endpoint Usage Guide

Este documento explica cómo usar el modelo Chatterbox Multilingual TTS deployado en Hugging Face Inference Endpoints.

## 📋 Tabla de Contenidos

- [Formato de Request](#formato-de-request)
- [Parámetros](#parámetros)
- [Ejemplos de Uso](#ejemplos-de-uso)
- [Idiomas Soportados](#idiomas-soportados)
- [Manejo de Errores](#manejo-de-errores)

## 🚀 Formato de Request

### Request Básico

```json
{
  "inputs": "Texto a sintetizar",
  "parameters": {
    "language_id": "es"
  }
}
```

### Request Completo

```json
{
  "inputs": "Texto a sintetizar (máximo 300 caracteres)",
  "parameters": {
    "language_id": "es",
    "audio_prompt_base64": "base64_encoded_audio_data",
    "exaggeration": 0.5,
    "temperature": 0.8,
    "cfg_weight": 0.5,
    "seed": 0,
    "return_format": "base64"
  }
}
```

## 📝 Parámetros

### Requeridos

| Parámetro | Tipo | Descripción |
|-----------|------|-------------|
| `inputs` | string | Texto a sintetizar (máximo 300 caracteres) |
| `language_id` | string | Código de idioma (ver tabla abajo) |

### Opcionales

| Parámetro | Tipo | Rango | Default | Descripción |
|-----------|------|-------|---------|-------------|
| `audio_prompt_base64` | string | - | null | Audio de referencia codificado en base64 para clonar voz |
| `exaggeration` | float | 0.25-2.0 | 0.5 | Control de expresividad (0.5 = neutral) |
| `temperature` | float | 0.05-5.0 | 0.8 | Control de aleatoriedad (mayor = más variado) |
| `cfg_weight` | float | 0.2-1.0 | 0.5 | Peso de guía CFG/Pace (0 para transferencia de idioma) |
| `seed` | int | ≥0 | 0 | Semilla aleatoria (0 = aleatorio) |
| `return_format` | string | "base64" o "array" | "base64" | Formato de retorno del audio |

## 💡 Ejemplos de Uso

### Python

#### Ejemplo 1: Generación Básica

```python
import requests
import base64
import io
from pydub import AudioSegment

# URL del endpoint (reemplaza con tu URL)
ENDPOINT_URL = "https://your-endpoint.endpoints.huggingface.cloud"
HEADERS = {
    "Authorization": "Bearer YOUR_HF_TOKEN",
    "Content-Type": "application/json"
}

# Request básico
payload = {
    "inputs": "Hola, este es un ejemplo de síntesis de voz en español.",
    "parameters": {
        "language_id": "es",
        "exaggeration": 0.5,
        "temperature": 0.8
    }
}

response = requests.post(ENDPOINT_URL, headers=HEADERS, json=payload)
result = response.json()

# Decodificar y guardar audio
if "audio" in result:
    audio_data = base64.b64decode(result["audio"])
    with open("output.wav", "wb") as f:
        f.write(audio_data)
    print(f"✅ Audio generado: {result['sample_rate']} Hz")
else:
    print(f"❌ Error: {result.get('error')}")
```

#### Ejemplo 2: Con Audio de Referencia

```python
import base64

# Leer audio de referencia
with open("reference_voice.wav", "rb") as f:
    audio_bytes = f.read()
    audio_base64 = base64.b64encode(audio_bytes).decode('utf-8')

# Request con audio de referencia
payload = {
    "inputs": "Este texto usará la voz del audio de referencia.",
    "parameters": {
        "language_id": "es",
        "audio_prompt_base64": audio_base64,
        "exaggeration": 0.7,
        "cfg_weight": 0.5
    }
}

response = requests.post(ENDPOINT_URL, headers=HEADERS, json=payload)
result = response.json()

# Guardar resultado
if "audio" in result:
    audio_data = base64.b64decode(result["audio"])
    with open("cloned_voice.wav", "wb") as f:
        f.write(audio_data)
```

#### Ejemplo 3: Múltiples Idiomas

```python
languages = {
    "en": "Hello, this is a test in English.",
    "es": "Hola, esta es una prueba en español.",
    "fr": "Bonjour, ceci est un test en français.",
    "de": "Hallo, das ist ein Test auf Deutsch."
}

for lang_code, text in languages.items():
    payload = {
        "inputs": text,
        "parameters": {
            "language_id": lang_code
        }
    }
    
    response = requests.post(ENDPOINT_URL, headers=HEADERS, json=payload)
    result = response.json()
    
    if "audio" in result:
        audio_data = base64.b64decode(result["audio"])
        with open(f"output_{lang_code}.wav", "wb") as f:
            f.write(audio_data)
        print(f"✅ {lang_code}: Audio generado")
```

### JavaScript/Node.js

```javascript
const axios = require('axios');
const fs = require('fs');

const ENDPOINT_URL = "https://your-endpoint.endpoints.huggingface.cloud";
const HF_TOKEN = "YOUR_HF_TOKEN";

async function generateTTS(text, languageId) {
    try {
        const response = await axios.post(
            ENDPOINT_URL,
            {
                inputs: text,
                parameters: {
                    language_id: languageId,
                    exaggeration: 0.5,
                    temperature: 0.8
                }
            },
            {
                headers: {
                    'Authorization': `Bearer ${HF_TOKEN}`,
                    'Content-Type': 'application/json'
                }
            }
        );

        if (response.data.audio) {
            const audioBuffer = Buffer.from(response.data.audio, 'base64');
            fs.writeFileSync('output.wav', audioBuffer);
            console.log('✅ Audio generado exitosamente');
        } else {
            console.error('❌ Error:', response.data.error);
        }
    } catch (error) {
        console.error('❌ Request failed:', error.message);
    }
}

// Uso
generateTTS("Hola mundo", "es");
```

### cURL

```bash
curl -X POST "https://your-endpoint.endpoints.huggingface.cloud" \
  -H "Authorization: Bearer YOUR_HF_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "inputs": "Hola, este es un ejemplo de síntesis de voz.",
    "parameters": {
      "language_id": "es",
      "exaggeration": 0.5,
      "temperature": 0.8
    }
  }' | jq -r '.audio' | base64 -d > output.wav
```

## 🌍 Idiomas Soportados

| Código | Idioma | Código | Idioma |
|--------|--------|--------|--------|
| `ar` | Árabe | `ms` | Malayo |
| `da` | Danés | `nl` | Holandés |
| `de` | Alemán | `no` | Noruego |
| `el` | Griego | `pl` | Polaco |
| `en` | Inglés | `pt` | Portugués |
| `es` | Español | `ru` | Ruso |
| `fi` | Finlandés | `sv` | Sueco |
| `fr` | Francés | `sw` | Suajili |
| `he` | Hebreo | `tr` | Turco |
| `hi` | Hindi | `zh` | Chino |
| `it` | Italiano | | |
| `ja` | Japonés | | |
| `ko` | Coreano | | |

**Total: 23 idiomas soportados**

## ⚠️ Manejo de Errores

### Respuesta de Error

```json
{
  "error": "Descripción del error"
}
```

### Errores Comunes

| Error | Causa | Solución |
|-------|-------|----------|
| `Missing or invalid 'inputs' field` | No se proporcionó texto | Incluir campo `inputs` con texto válido |
| `Unsupported language 'xx'` | Código de idioma inválido | Usar uno de los 23 códigos soportados |
| `Failed to decode audio prompt` | Audio base64 inválido | Verificar codificación del audio de referencia |
| `Inference failed` | Error durante generación | Revisar parámetros y logs del endpoint |

## 📊 Formato de Respuesta

### Respuesta Exitosa (base64)

```json
{
  "audio": "UklGRiQAAABXQVZFZm10IBAAAAABAAEA...",
  "sample_rate": 24000,
  "language": "es",
  "text": "Texto sintetizado",
  "format": "wav_base64"
}
```

### Respuesta Exitosa (array)

```json
{
  "audio": [0.001, -0.002, 0.003, ...],
  "sample_rate": 24000,
  "language": "es",
  "text": "Texto sintetizado"
}
```

## 🎯 Mejores Prácticas

1. **Longitud del Texto**: Mantener textos bajo 300 caracteres para mejor calidad
2. **Audio de Referencia**: Usar clips de 3-10 segundos en el idioma objetivo
3. **Exageración**: Valores extremos (< 0.3 o > 1.5) pueden ser inestables
4. **CFG Weight**: Usar 0 para transferencia de idioma con acento del audio de referencia
5. **Temperatura**: Valores más bajos (0.3-0.5) para mayor consistencia
6. **Rate Limiting**: Implementar retry logic para manejar límites de tasa

## 🔧 Testing Local

Antes de deployar, puedes probar el handler localmente:

```bash
python test_handler.py
```

## 📚 Recursos Adicionales

- [Documentación de Hugging Face Inference Endpoints](https://huggingface.co/docs/inference-endpoints)
- [Repositorio del Modelo](https://huggingface.co/ResembleAI/chatterbox)
- [Demo en Gradio](https://huggingface.co/spaces/ResembleAI/chatterbox)
