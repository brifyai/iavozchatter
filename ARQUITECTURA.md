# 🏗️ Arquitectura del Endpoint

Este documento explica cómo funciona el endpoint de Chatterbox Multilingual TTS deployado en Hugging Face.

## 📊 Diagrama de Flujo

```
┌─────────────────────────────────────────────────────────────────┐
│                         CLIENTE                                  │
│  (Python, JavaScript, cURL, etc.)                               │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         │ HTTP POST Request
                         │ {
                         │   "inputs": "texto",
                         │   "parameters": {"language_id": "es"}
                         │ }
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│              HUGGING FACE INFERENCE ENDPOINT                     │
│                                                                  │
│  ┌────────────────────────────────────────────────────────┐    │
│  │                    handler.py                           │    │
│  │                                                         │    │
│  │  class EndpointHandler:                                │    │
│  │                                                         │    │
│  │    def __init__(self, path=""):                        │    │
│  │        # Carga el modelo al iniciar                    │    │
│  │        self.model = ChatterboxMultilingualTTS...       │    │
│  │                                                         │    │
│  │    def __call__(self, data):                           │    │
│  │        # Procesa cada request                          │    │
│  │        text = data["inputs"]                           │    │
│  │        params = data["parameters"]                     │    │
│  │        wav = self.model.generate(...)                  │    │
│  │        return {"audio": base64(wav), ...}              │    │
│  └────────────────────────────────────────────────────────┘    │
│                         │                                        │
│                         ▼                                        │
│  ┌────────────────────────────────────────────────────────┐    │
│  │           ChatterboxMultilingualTTS                     │    │
│  │                                                         │    │
│  │  ┌──────────────┐  ┌──────────────┐  ┌─────────────┐ │    │
│  │  │  Tokenizer   │  │  T3 Model    │  │  S3Gen      │ │    │
│  │  │  (MTL)       │  │  (LLM-based) │  │  (Vocoder)  │ │    │
│  │  └──────────────┘  └──────────────┘  └─────────────┘ │    │
│  │         │                  │                  │        │    │
│  │         └──────────────────┴──────────────────┘        │    │
│  │                         │                               │    │
│  │  ┌──────────────────────▼────────────────────────┐    │    │
│  │  │        Voice Encoder (opcional)               │    │    │
│  │  │        Para clonación de voz                  │    │    │
│  │  └───────────────────────────────────────────────┘    │    │
│  └────────────────────────────────────────────────────────┘    │
│                         │                                        │
│                    GPU (A10G/A100)                              │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         │ HTTP Response
                         │ {
                         │   "audio": "base64_encoded_wav",
                         │   "sample_rate": 24000,
                         │   "language": "es"
                         │ }
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                         CLIENTE                                  │
│  Decodifica base64 → Guarda/Reproduce audio WAV                 │
└─────────────────────────────────────────────────────────────────┘
```

## 🔄 Flujo de Procesamiento Detallado

### 1. Inicialización (Una vez al arrancar)

```python
# handler.py - __init__()
┌─────────────────────────────────────────┐
│ 1. Detectar dispositivo (CUDA/CPU)     │
│ 2. Cargar Voice Encoder (ve.pt)        │
│ 3. Cargar T3 Model (t3_mtl23ls_v2)     │
│ 4. Cargar S3Gen (s3gen.pt)             │
│ 5. Cargar Tokenizer (grapheme_mtl...)  │
│ 6. Cargar condiciones default (conds)  │
└─────────────────────────────────────────┘
         │
         ▼
   Modelo listo para inferencia
```

### 2. Procesamiento de Request (Por cada llamada)

```python
# handler.py - __call__()
┌─────────────────────────────────────────┐
│ 1. Validar inputs                       │
│    - Texto presente?                    │
│    - Idioma soportado?                  │
│    - Parámetros válidos?                │
└─────────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────┐
│ 2. Preparar parámetros                  │
│    - Truncar texto a 300 chars          │
│    - Extraer language_id                │
│    - Configurar exaggeration, temp, etc │
│    - Decodificar audio_prompt si existe │
└─────────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────┐
│ 3. Generar audio                        │
│    a) Normalizar puntuación             │
│    b) Tokenizar texto                   │
│    c) Preparar condiciones              │
│    d) T3: Generar speech tokens         │
│    e) S3Gen: Tokens → Audio waveform    │
│    f) Aplicar watermark                 │
└─────────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────┐
│ 4. Formatear respuesta                  │
│    - Convertir numpy → base64           │
│    - Crear JSON response                │
│    - Incluir metadata                   │
└─────────────────────────────────────────┘
         │
         ▼
   Retornar respuesta al cliente
```

## 🧩 Componentes del Sistema

### Handler Layer (handler.py)

```
┌──────────────────────────────────────────────────────┐
│                  EndpointHandler                      │
├──────────────────────────────────────────────────────┤
│ Responsabilidades:                                   │
│ • Validación de inputs                               │
│ • Manejo de errores                                  │
│ • Conversión de formatos (base64 ↔ audio)           │
│ • Interfaz HTTP/REST                                 │
└──────────────────────────────────────────────────────┘
```

### Model Layer (ChatterboxMultilingualTTS)

```
┌──────────────────────────────────────────────────────┐
│           ChatterboxMultilingualTTS                   │
├──────────────────────────────────────────────────────┤
│ Componentes:                                         │
│                                                      │
│ ┌────────────────┐  ┌──────────────────────────┐   │
│ │  MTLTokenizer  │  │  Convierte texto a IDs   │   │
│ │                │  │  Soporta 23 idiomas      │   │
│ └────────────────┘  └──────────────────────────┘   │
│                                                      │
│ ┌────────────────┐  ┌──────────────────────────┐   │
│ │  T3 Model      │  │  LLM-based TTS           │   │
│ │  (Transformer) │  │  Texto → Speech Tokens   │   │
│ └────────────────┘  └──────────────────────────┘   │
│                                                      │
│ ┌────────────────┐  ┌──────────────────────────┐   │
│ │  S3Gen         │  │  Neural Vocoder          │   │
│ │  (Vocoder)     │  │  Tokens → Audio (24kHz)  │   │
│ └────────────────┘  └──────────────────────────┘   │
│                                                      │
│ ┌────────────────┐  ┌──────────────────────────┐   │
│ │ VoiceEncoder   │  │  Extrae características  │   │
│ │                │  │  Para clonación de voz   │   │
│ └────────────────┘  └──────────────────────────┘   │
└──────────────────────────────────────────────────────┘
```

## 📦 Archivos del Modelo

```
Repositorio en Hugging Face
│
├── handler.py                          # Handler personalizado
├── requirements.txt                    # Dependencias
│
├── Archivos del modelo (pesos)
│   ├── ve.pt                          # Voice Encoder (50MB)
│   ├── t3_mtl23ls_v2.safetensors     # T3 Model (1.5GB)
│   ├── s3gen.pt                       # S3Gen Vocoder (200MB)
│   └── conds.pt                       # Condiciones default (10MB)
│
├── Configuración
│   ├── grapheme_mtl_merged_expanded_v1.json  # Tokenizer
│   └── Cangjie5_TC.json               # Para chino
│
└── Código fuente
    └── src/chatterbox/                # Implementación del modelo
        ├── mtl_tts.py
        ├── models/
        │   ├── t3/
        │   ├── s3gen/
        │   ├── s3tokenizer/
        │   ├── tokenizers/
        │   └── voice_encoder/
        └── ...
```

## 🔐 Flujo de Autenticación

```
Cliente
  │
  │ Authorization: Bearer HF_TOKEN
  │
  ▼
Hugging Face API Gateway
  │
  │ Valida token
  │
  ▼
Endpoint Container
  │
  │ Procesa request
  │
  ▼
Respuesta
```

## ⚡ Optimizaciones

### Carga del Modelo (Cold Start)

```
Primera request (Cold Start):
┌─────────────────────────────────────┐
│ 1. Iniciar contenedor      ~30s     │
│ 2. Instalar dependencias    ~60s    │
│ 3. Descargar modelo         ~120s   │
│ 4. Cargar modelo en GPU     ~30s    │
│ 5. Primera inferencia       ~10s    │
├─────────────────────────────────────┤
│ TOTAL: ~4-5 minutos                 │
└─────────────────────────────────────┘

Requests subsecuentes (Warm):
┌─────────────────────────────────────┐
│ 1. Inferencia               ~5-10s  │
├─────────────────────────────────────┤
│ TOTAL: ~5-10 segundos               │
└─────────────────────────────────────┘
```

### Caching

El modelo permanece en memoria entre requests:
- ✅ Modelo cargado una sola vez
- ✅ GPU memory persistente
- ✅ Warm start para requests subsecuentes

## 📊 Recursos del Sistema

### GPU Memory Usage

```
┌─────────────────────────────────────────┐
│ Componente          │ VRAM              │
├─────────────────────┼───────────────────┤
│ T3 Model            │ ~3.5 GB           │
│ S3Gen Vocoder       │ ~1.0 GB           │
│ Voice Encoder       │ ~0.5 GB           │
│ Activations         │ ~1.0 GB           │
├─────────────────────┼───────────────────┤
│ TOTAL               │ ~6 GB             │
└─────────────────────────────────────────┘

Recomendación:
• Mínimo: A10G (24GB VRAM) ✅
• Óptimo: A100 (40GB VRAM) ✅✅
```

### Latencia por Componente

```
┌─────────────────────────────────────────┐
│ Paso                │ Tiempo            │
├─────────────────────┼───────────────────┤
│ Validación          │ <1ms              │
│ Tokenización        │ ~10ms             │
│ T3 Inference        │ ~3-5s             │
│ S3Gen Vocoder       │ ~2-3s             │
│ Encoding base64     │ ~100ms            │
├─────────────────────┼───────────────────┤
│ TOTAL               │ ~5-10s            │
└─────────────────────────────────────────┘
```

## 🔄 Escalabilidad

### Auto-scaling

```
Tráfico bajo:
┌─────────────┐
│ Replica 1   │ (Min replicas = 1)
└─────────────┘

Tráfico medio:
┌─────────────┐  ┌─────────────┐
│ Replica 1   │  │ Replica 2   │
└─────────────┘  └─────────────┘

Tráfico alto:
┌─────────────┐  ┌─────────────┐  ┌─────────────┐
│ Replica 1   │  │ Replica 2   │  │ Replica 3   │
└─────────────┘  └─────────────┘  └─────────────┘
                                   (Max replicas)
```

### Load Balancing

```
                  ┌─────────────────┐
                  │  Load Balancer  │
                  └────────┬────────┘
                           │
        ┌──────────────────┼──────────────────┐
        │                  │                  │
        ▼                  ▼                  ▼
┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│  Endpoint 1  │  │  Endpoint 2  │  │  Endpoint 3  │
└──────────────┘  └──────────────┘  └──────────────┘
```

## 🛡️ Seguridad

### Capas de Seguridad

```
1. Autenticación
   └─ Token de Hugging Face requerido

2. Rate Limiting
   └─ Límite de requests por minuto

3. Validación de Inputs
   └─ Sanitización en handler.py

4. Aislamiento
   └─ Contenedor Docker aislado

5. Logs
   └─ Auditoría de todos los requests
```

## 📈 Monitoreo

### Métricas Disponibles

```
┌─────────────────────────────────────────┐
│ Métrica             │ Descripción       │
├─────────────────────┼───────────────────┤
│ Requests/min        │ Throughput        │
│ Latencia promedio   │ Performance       │
│ Error rate          │ Reliability       │
│ GPU utilization     │ Resource usage    │
│ Memory usage        │ Resource usage    │
│ Queue depth         │ Load              │
└─────────────────────────────────────────┘
```

## 🎯 Mejores Prácticas

1. **Warm-up**: Hacer requests de prueba después del deployment
2. **Caching**: Implementar cache en el cliente para textos repetidos
3. **Batch**: Agrupar múltiples requests cuando sea posible
4. **Retry**: Implementar retry logic con exponential backoff
5. **Timeout**: Configurar timeouts apropiados (30-60s)
6. **Monitoring**: Vigilar métricas y configurar alertas

## 📚 Referencias

- [handler.py](./handler.py) - Implementación del handler
- [DEPLOYMENT.md](./DEPLOYMENT.md) - Guía de deployment
- [ENDPOINT_USAGE.md](./ENDPOINT_USAGE.md) - Documentación de uso
