from typing import Dict, List, Any
import torch
import numpy as np
import base64
import io
import soundfile as sf
from pathlib import Path
import tempfile
import os

from src.chatterbox.mtl_tts import ChatterboxMultilingualTTS


class EndpointHandler:
    """
    Handler personalizado para síntesis de voz en español con Chatterbox TTS.
    
    Formato de entrada esperado:
    {
        "inputs": "Texto a sintetizar en español",
        "parameters": {
            "audio_prompt_base64": "audio_referencia_base64",  # Opcional: audio de referencia
            "exaggeration": 0.5,  # Opcional: 0.25-2.0, default 0.5 (expresividad)
            "temperature": 0.8,  # Opcional: 0.05-5.0, default 0.8 (variabilidad)
            "cfg_weight": 0.5,  # Opcional: 0.2-1.0, default 0.5 (control de ritmo)
            "seed": 0,  # Opcional: semilla aleatoria, 0 para aleatorio
            "return_format": "base64"  # Opcional: "base64" o "array", default "base64"
        }
    }
    
    Retorna:
    {
        "audio": "audio_wav_codificado_base64" o array numpy,
        "sample_rate": 24000,
        "text": "texto sintetizado"
    }
    """
    
    def __init__(self, path: str = ""):
        """Inicializa el modelo cuando arranca el endpoint."""
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        print(f"🚀 Iniciando Chatterbox TTS en español - Dispositivo: {self.device}")
        
        # Cargar modelo desde el repositorio
        if path and Path(path).exists():
            print(f"Cargando modelo desde ruta local: {path}")
            self.model = ChatterboxMultilingualTTS.from_local(path, self.device)
        else:
            print("Cargando modelo desde Hugging Face Hub")
            self.model = ChatterboxMultilingualTTS.from_pretrained(self.device)
        
        self.sample_rate = self.model.sr
        self.language = "es"  # Solo español
        print(f"✅ Modelo cargado exitosamente. Frecuencia de muestreo: {self.sample_rate} Hz")
    
    def __call__(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Procesa la solicitud y genera el audio TTS en español.
        
        Args:
            data: Diccionario con 'inputs' (texto) y 'parameters' opcionales
        
        Returns:
            Diccionario con el audio generado y metadata
        """
        try:
            # Extraer el texto de entrada
            text = data.get("inputs", "")
            if not text or not isinstance(text, str):
                return {"error": "Falta el campo 'inputs' o es inválido. Por favor proporciona el texto a sintetizar."}
            
            # Truncar texto a máximo 300 caracteres
            text = text[:300]
            
            # Extraer parámetros opcionales
            params = data.get("parameters", {})
            
            # Parámetros con valores por defecto optimizados para español natural
            exaggeration = float(params.get("exaggeration", 0.6))  # Más expresivo para español
            temperature = float(params.get("temperature", 0.85))  # Más natural
            cfg_weight = float(params.get("cfg_weight", 0.5))
            seed = int(params.get("seed", 0))
            return_format = params.get("return_format", "base64")
            
            # Configurar semilla si se especifica
            if seed != 0:
                torch.manual_seed(seed)
                if self.device == "cuda":
                    torch.cuda.manual_seed(seed)
                    torch.cuda.manual_seed_all(seed)
            
            # Manejar audio de referencia opcional (codificado en base64)
            audio_prompt_path = None
            if "audio_prompt_base64" in params:
                audio_prompt_path = self._decode_audio_prompt(params["audio_prompt_base64"])
            
            # Generar audio
            print(f"Generando voz en español para: '{text[:50]}...'")
            
            generate_kwargs = {
                "exaggeration": exaggeration,
                "temperature": temperature,
                "cfg_weight": cfg_weight,
            }
            
            if audio_prompt_path:
                generate_kwargs["audio_prompt_path"] = audio_prompt_path
            
            wav = self.model.generate(
                text,
                language_id=self.language,  # Siempre español
                **generate_kwargs
            )
            
            # Convertir a numpy
            wav_np = wav.squeeze(0).numpy()
            
            # Limpiar archivo temporal si se creó
            if audio_prompt_path and os.path.exists(audio_prompt_path):
                os.remove(audio_prompt_path)
            
            # Formatear respuesta
            if return_format == "array":
                return {
                    "audio": wav_np.tolist(),
                    "sample_rate": self.sample_rate,
                    "text": text
                }
            else:
                # Retornar audio codificado en base64
                audio_base64 = self._encode_audio_to_base64(wav_np, self.sample_rate)
                return {
                    "audio": audio_base64,
                    "sample_rate": self.sample_rate,
                    "text": text,
                    "format": "wav_base64"
                }
        
        except Exception as e:
            print(f"Error durante la inferencia: {str(e)}")
            return {"error": f"La generación falló: {str(e)}"}
    
    def _decode_audio_prompt(self, base64_audio: str) -> str:
        """Decodifica audio en base64 y lo guarda en archivo temporal."""
        try:
            audio_bytes = base64.b64decode(base64_audio)
            
            # Crear archivo temporal
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
            temp_file.write(audio_bytes)
            temp_file.close()
            
            return temp_file.name
        except Exception as e:
            raise ValueError(f"Error al decodificar el audio de referencia: {str(e)}")
    
    def _encode_audio_to_base64(self, audio_array: np.ndarray, sample_rate: int) -> str:
        """Codifica el array de audio a formato WAV en base64."""
        buffer = io.BytesIO()
        sf.write(buffer, audio_array, sample_rate, format='WAV')
        buffer.seek(0)
        audio_base64 = base64.b64encode(buffer.read()).decode('utf-8')
        return audio_base64
