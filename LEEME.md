# 🎯 Guía Rápida de Deployment

## ¿Qué se ha creado?

He preparado todo lo necesario para deployar tu modelo Chatterbox Multilingual TTS en Hugging Face Inference Endpoints. Aquí está lo que tienes:

### 📄 Archivos Principales

1. **handler.py** ⭐ - El archivo más importante. Contiene el código que Hugging Face usa para procesar requests.

2. **requirements.txt** - Actualizado con todas las dependencias necesarias.

### 📚 Documentación Completa

3. **DEPLOYMENT.md** - Guía paso a paso para deployar (¡EMPIEZA AQUÍ!)

4. **ENDPOINT_USAGE.md** - Cómo usar el endpoint una vez deployado

5. **CHECKLIST.md** - Lista de verificación para el deployment

6. **RESUMEN.md** - Resumen ejecutivo de todo

7. **examples_multilang.md** - Ejemplos en Python, JavaScript, PHP, Go, Ruby, C#, cURL

### 💻 Código de Ejemplo

8. **example_client.py** - Cliente Python listo para usar

9. **test_handler.py** - Script para probar localmente antes de deployar

## 🚀 Pasos Rápidos

### 1. Subir archivos a Hugging Face

```bash
cd Chatterbox-Multilingual-TTS

# Agregar archivos
git add handler.py requirements.txt *.md example_client.py test_handler.py

# Commit
git commit -m "Add custom handler for Inference Endpoints"

# Push
git push
```

### 2. Verificar que tienes los archivos del modelo

Asegúrate de que estos archivos estén en tu repositorio:
- ✅ ve.pt
- ✅ t3_mtl23ls_v2.safetensors
- ✅ s3gen.pt
- ✅ grapheme_mtl_merged_expanded_v1.json
- ✅ conds.pt
- ✅ src/chatterbox/ (carpeta completa)

### 3. Crear el Endpoint

Ve a https://ui.endpoints.huggingface.co/ y:
1. Click "New Endpoint"
2. Selecciona tu repositorio
3. Configura:
   - Instance: GPU [medium] - 1x Nvidia A10G (mínimo)
   - Region: us-east-1 (o la más cercana)
4. Click "Create Endpoint"

### 4. Esperar 5-15 minutos

El endpoint se está deployando. Puedes ver el progreso en los logs.

### 5. Probar

```python
import requests
import base64

ENDPOINT_URL = "https://tu-endpoint.endpoints.huggingface.cloud"
HEADERS = {"Authorization": "Bearer TU_HF_TOKEN"}

response = requests.post(
    ENDPOINT_URL,
    headers=HEADERS,
    json={
        "inputs": "Hola, este es un test.",
        "parameters": {"language_id": "es"}
    }
)

# Guardar audio
audio_data = base64.b64decode(response.json()["audio"])
with open("test.wav", "wb") as f:
    f.write(audio_data)
```

## 📖 ¿Qué leer primero?

1. **DEPLOYMENT.md** - Para deployar el modelo
2. **ENDPOINT_USAGE.md** - Para usar el endpoint
3. **example_client.py** - Para ver código de ejemplo

## 🆘 ¿Problemas?

### "No handler.py file was found"
→ Asegúrate de que `handler.py` está en la raíz del repo

### "Module not found"
→ Verifica que `requirements.txt` tiene todas las dependencias

### "Model files not found"
→ Asegúrate de que los archivos .pt y .safetensors están en el repo

### Endpoint muy lento
→ Aumenta el tamaño de la instancia GPU

Más soluciones en **DEPLOYMENT.md** sección "Troubleshooting"

## 🌍 Idiomas Soportados (23)

ar, da, de, el, en, es, fi, fr, he, hi, it, ja, ko, ms, nl, no, pl, pt, ru, sv, sw, tr, zh

## 💰 Costos Aproximados

- GPU [medium] A10G: ~$1.30/hora
- GPU [xlarge] A100: ~$4.50/hora

Usa auto-scaling para reducir costos cuando no hay tráfico.

## ✅ Checklist Rápido

- [ ] Archivos subidos a Hugging Face
- [ ] handler.py en la raíz
- [ ] Archivos del modelo (.pt, .safetensors) en el repo
- [ ] Endpoint creado
- [ ] Estado = "running"
- [ ] Test básico funciona

## 🎉 ¡Listo!

Si tienes todo marcado, tu modelo está deployado y listo para usar.

Para más detalles, consulta **DEPLOYMENT.md** y **ENDPOINT_USAGE.md**.

---

**Archivos creados**:
- handler.py (código principal)
- 7 archivos de documentación (.md)
- 2 scripts de ejemplo (.py)
- requirements.txt (actualizado)

**Total**: 11 archivos nuevos/actualizados
