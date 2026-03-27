# 🎙️ Chatterbox TTS - Español

## ¿Qué es?

Un sistema que convierte texto a voz en español. La voz suena natural y humana.

## ¿Cómo funciona?

Le envías texto → Te devuelve audio

## Uso Básico

```python
import requests
import base64

# Enviar texto
response = requests.post(
    "https://tu-endpoint.endpoints.huggingface.cloud",
    headers={"Authorization": "Bearer TU_TOKEN"},
    json={"inputs": "Hola, ¿cómo estás?"}
)

# Recibir audio
audio = base64.b64decode(response.json()["audio"])
with open("voz.wav", "wb") as f:
    f.write(audio)
```

## Personalizar la Voz

```python
# Voz neutral (noticias, informes)
{"inputs": "...", "parameters": {"exaggeration": 0.4}}

# Voz natural (conversaciones)
{"inputs": "...", "parameters": {"exaggeration": 0.6}}

# Voz expresiva (publicidad, emoción)
{"inputs": "...", "parameters": {"exaggeration": 1.0}}
```

## Deployment

1. Sube `handler.py` y `requirements.txt` a Hugging Face
2. Crea un endpoint en https://ui.endpoints.huggingface.co/
3. Espera 5-10 minutos
4. ¡Listo!

## Archivos Importantes

- **GUIA_RAPIDA.md** - Empieza aquí (5 minutos)
- **EJEMPLOS_USO.md** - Casos de uso reales
- **example_client.py** - Código listo para usar
- **test_handler.py** - Prueba antes de deployar

## Características

✅ Voz natural en español  
✅ Control de expresividad  
✅ Clonación de voz  
✅ API REST  
✅ Audio 24kHz  

## Costos

~$1.30/hora (GPU A10G)

## Soporte

- Documentación: Ver archivos .md
- Ejemplos: Ver example_client.py
- Pruebas: Ejecutar test_handler.py

---

**Lee GUIA_RAPIDA.md para empezar →**
