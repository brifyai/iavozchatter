"""
Handler para RunPod Serverless
Optimizado para síntesis de voz en español con Chatterbox TTS
"""

import runpod
import torch
import numpy as np
import base64
import io
import soundfile as sf
from pathlib import Path
import os
import sys

from src.chatterbox.mtl_tts import ChatterboxMultilingualTTS


# Cargar modelo globalmente (una sola vez)
print("🚀 Iniciando Chatterbox TTS en español...", flush=True)
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
print(f"Dispositivo: {DEVICE}", flush=True)

try:
    MODEL = ChatterboxMultilingualTTS.from_pretrained(DEVICE)
    SAMPLE_RATE = MODEL.sr
    LANGUAGE = "es"
    print(f"✅ Modelo cargado. Frecuencia: {SAMPLE_RATE} Hz", flush=True)
except Exception as e:
    print(f"❌ Error al cargar modelo: {str(e)}", flush=True)
    sys.exit(1)


def generar_audio(texto: str, params: dict) -> dict:
    """
    Genera audio de voz en español.
    
    Args:
        texto: Texto a sintetizar
        params: Parámetros de generación
    
    Returns:
        Diccionario con audio en base64 y metadata
    """
    try:
        # Truncar texto
        texto = texto[:300]
        
        # Parámetros con defaults optimizados para español
        expresividad = float(params.get("exaggeration", 0.6))
        temperatura = float(params.get("temperature", 0.85))
        peso_cfg = float(params.get("cfg_weight", 0.5))
        semilla = int(params.get("seed", 0))
        
        # Configurar semilla
        if semilla != 0:
            torch.manual_seed(semilla)
            if DEVICE == "cuda":
                torch.cuda.manual_seed_all(semilla)
        
        print(f"Generando: '{texto[:50]}...'", flush=True)
        
        # Generar audio
        wav = MODEL.generate(
            texto,
            language_id=LANGUAGE,
            exaggeration=expresividad,
            temperature=temperatura,
            cfg_weight=peso_cfg,
        )
        
        # Convertir a numpy
        wav_np = wav.squeeze(0).numpy()
        
        # Codificar a base64
        buffer = io.BytesIO()
        sf.write(buffer, wav_np, SAMPLE_RATE, format='WAV')
        buffer.seek(0)
        audio_base64 = base64.b64encode(buffer.read()).decode('utf-8')
        
        return {
            "audio": audio_base64,
            "sample_rate": SAMPLE_RATE,
            "text": texto,
            "format": "wav_base64"
        }
        
    except Exception as e:
        print(f"❌ Error: {str(e)}", flush=True)
        raise Exception(f"Error al generar audio: {str(e)}")


def handler(job):
    """
    Handler principal de RunPod.
    
    Formato de entrada:
    {
        "input": {
            "texto": "Texto a sintetizar",
            "exaggeration": 0.6,
            "temperature": 0.85,
            "cfg_weight": 0.5,
            "seed": 0
        }
    }
    """
    try:
        job_input = job["input"]
        
        # Extraer texto
        texto = job_input.get("texto") or job_input.get("text") or job_input.get("inputs")
        
        if not texto:
            return {
                "error": "Falta el campo 'texto'. Proporciona el texto a sintetizar."
            }
        
        # Generar audio
        resultado = generar_audio(texto, job_input)
        
        return resultado
        
    except Exception as e:
        return {"error": str(e)}


# Iniciar el worker de RunPod
if __name__ == "__main__":
    print("🚀 Iniciando RunPod worker...", flush=True)
    print("✅ Worker listo para recibir requests", flush=True)
    
    # Mantener el proceso vivo
    runpod.serverless.start({"handler": handler})
