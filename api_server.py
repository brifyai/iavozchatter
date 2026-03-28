"""
Servidor API para RunPod Pod (no serverless)
Expone endpoint HTTP en puerto 8000
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import torch
import numpy as np
import base64
import io
import soundfile as sf
import uvicorn
from typing import Optional

from src.chatterbox.mtl_tts import ChatterboxMultilingualTTS

# Crear app FastAPI
app = FastAPI(title="Chatterbox TTS API", version="1.0")

# Cargar modelo globalmente
print("🚀 Iniciando Chatterbox TTS en español...")
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
print(f"Dispositivo: {DEVICE}")

MODEL = ChatterboxMultilingualTTS.from_pretrained(DEVICE)
SAMPLE_RATE = MODEL.sr
LANGUAGE = "es"

print(f"✅ Modelo cargado. Frecuencia: {SAMPLE_RATE} Hz")


# Modelo de request
class TTSRequest(BaseModel):
    texto: str
    exaggeration: Optional[float] = 0.6
    temperature: Optional[float] = 0.85
    cfg_weight: Optional[float] = 0.5
    seed: Optional[int] = 0


# Modelo de response
class TTSResponse(BaseModel):
    audio: str
    sample_rate: int
    text: str
    format: str = "wav_base64"


@app.get("/")
async def root():
    """Endpoint de health check"""
    return {
        "status": "running",
        "model": "Chatterbox TTS Español",
        "device": DEVICE,
        "sample_rate": SAMPLE_RATE
    }


@app.get("/health")
async def health():
    """Health check detallado"""
    return {
        "status": "healthy",
        "model_loaded": MODEL is not None,
        "device": DEVICE,
        "cuda_available": torch.cuda.is_available()
    }


@app.post("/generate", response_model=TTSResponse)
async def generate_audio(request: TTSRequest):
    """
    Generar audio de voz en español
    
    Args:
        request: TTSRequest con texto y parámetros
    
    Returns:
        TTSResponse con audio en base64
    """
    try:
        # Truncar texto
        texto = request.texto[:300]
        
        if not texto:
            raise HTTPException(status_code=400, detail="El texto no puede estar vacío")
        
        # Configurar semilla
        if request.seed != 0:
            torch.manual_seed(request.seed)
            if DEVICE == "cuda":
                torch.cuda.manual_seed_all(request.seed)
        
        print(f"Generando: '{texto[:50]}...'")
        
        # Generar audio
        wav = MODEL.generate(
            texto,
            language_id=LANGUAGE,
            exaggeration=request.exaggeration,
            temperature=request.temperature,
            cfg_weight=request.cfg_weight,
        )
        
        # Convertir a numpy
        wav_np = wav.squeeze(0).numpy()
        
        # Codificar a base64
        buffer = io.BytesIO()
        sf.write(buffer, wav_np, SAMPLE_RATE, format='WAV')
        buffer.seek(0)
        audio_base64 = base64.b64encode(buffer.read()).decode('utf-8')
        
        return TTSResponse(
            audio=audio_base64,
            sample_rate=SAMPLE_RATE,
            text=texto
        )
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error al generar audio: {str(e)}")


if __name__ == "__main__":
    print("🚀 Iniciando servidor API en puerto 8000...")
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info"
    )
