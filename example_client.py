"""
Cliente de ejemplo para consumir el endpoint de Chatterbox TTS en español.
Reemplaza ENDPOINT_URL y HF_TOKEN con tus valores reales.
"""

import requests
import base64
import os
from pathlib import Path
from typing import Optional


class ChatterboxTTSClient:
    """Cliente para interactuar con el endpoint de Chatterbox TTS en español."""
    
    def __init__(self, endpoint_url: str, hf_token: str):
        """
        Inicializar el cliente.
        
        Args:
            endpoint_url: URL del endpoint de Hugging Face
            hf_token: Token de autenticación de Hugging Face
        """
        self.endpoint_url = endpoint_url
        self.headers = {
            "Authorization": f"Bearer {hf_token}",
            "Content-Type": "application/json"
        }
    
    def generar(
        self,
        texto: str,
        audio_referencia: Optional[str] = None,
        expresividad: float = 0.6,
        temperatura: float = 0.85,
        peso_cfg: float = 0.5,
        semilla: int = 0,
        archivo_salida: str = "audio_generado.wav"
    ) -> dict:
        """
        Generar audio de voz en español.
        
        Args:
            texto: Texto a sintetizar (máximo 300 caracteres)
            audio_referencia: Ruta al archivo de audio de referencia (opcional)
            expresividad: Control de expresividad (0.25-2.0, default 0.6)
            temperatura: Control de variabilidad (0.05-5.0, default 0.85)
            peso_cfg: Peso de control de ritmo (0.2-1.0, default 0.5)
            semilla: Semilla aleatoria (0 para aleatorio)
            archivo_salida: Ruta donde guardar el audio generado
        
        Returns:
            Diccionario con información de la respuesta
        """
        # Preparar payload
        payload = {
            "inputs": texto[:300],  # Truncar a 300 caracteres
            "parameters": {
                "exaggeration": expresividad,
                "temperature": temperatura,
                "cfg_weight": peso_cfg,
                "seed": semilla,
                "return_format": "base64"
            }
        }
        
        # Agregar audio de referencia si se proporciona
        if audio_referencia and os.path.exists(audio_referencia):
            with open(audio_referencia, "rb") as f:
                audio_bytes = f.read()
                audio_base64 = base64.b64encode(audio_bytes).decode('utf-8')
                payload["parameters"]["audio_prompt_base64"] = audio_base64
        
        # Hacer request
        try:
            response = requests.post(
                self.endpoint_url,
                headers=self.headers,
                json=payload,
                timeout=60
            )
            response.raise_for_status()
            result = response.json()
            
            # Verificar si hay error
            if "error" in result:
                print(f"❌ Error del servidor: {result['error']}")
                return result
            
            # Decodificar y guardar audio
            if "audio" in result:
                audio_data = base64.b64decode(result["audio"])
                
                # Crear directorio si no existe
                output_dir = Path(archivo_salida).parent
                if output_dir != Path('.'):
                    output_dir.mkdir(parents=True, exist_ok=True)
                
                with open(archivo_salida, "wb") as f:
                    f.write(audio_data)
                
                print(f"✅ Audio generado exitosamente:")
                print(f"   - Archivo: {archivo_salida}")
                print(f"   - Frecuencia: {result['sample_rate']} Hz")
                print(f"   - Texto: {result['text']}")
                
                result["archivo_salida"] = archivo_salida
            
            return result
            
        except requests.exceptions.Timeout:
            print("❌ Error: El servidor tardó demasiado en responder (>60s)")
            return {"error": "Timeout del servidor"}
        except requests.exceptions.RequestException as e:
            print(f"❌ Error en la conexión: {str(e)}")
            return {"error": str(e)}
        except Exception as e:
            print(f"❌ Error inesperado: {str(e)}")
            return {"error": str(e)}
    
    def generar_varios(
        self,
        textos: list[str],
        carpeta_salida: str = "audios_generados",
        **kwargs
    ) -> list[dict]:
        """
        Generar múltiples audios.
        
        Args:
            textos: Lista de textos a sintetizar
            carpeta_salida: Carpeta donde guardar los audios
            **kwargs: Parámetros adicionales para generar()
        
        Returns:
            Lista de diccionarios con resultados
        """
        resultados = []
        
        # Crear carpeta de salida
        Path(carpeta_salida).mkdir(parents=True, exist_ok=True)
        
        for i, texto in enumerate(textos):
            print(f"\n[{i+1}/{len(textos)}] Generando: {texto[:50]}...")
            
            archivo_salida = os.path.join(carpeta_salida, f"audio_{i+1}.wav")
            resultado = self.generar(
                texto=texto,
                archivo_salida=archivo_salida,
                **kwargs
            )
            resultados.append(resultado)
        
        return resultados


def main():
    """Ejemplos de uso del cliente."""
    
    # ⚠️ CONFIGURACIÓN - Reemplaza con tus valores
    ENDPOINT_URL = "https://tu-endpoint.endpoints.huggingface.cloud"
    HF_TOKEN = os.getenv("HF_TOKEN", "tu_token_aqui")
    
    # Verificar configuración
    if "tu-endpoint" in ENDPOINT_URL or "tu_token" in HF_TOKEN:
        print("⚠️  ADVERTENCIA: Debes configurar ENDPOINT_URL y HF_TOKEN")
        print("   Edita este archivo o configura la variable de entorno HF_TOKEN")
        return
    
    # Crear cliente
    cliente = ChatterboxTTSClient(ENDPOINT_URL, HF_TOKEN)
    
    print("=" * 70)
    print("Ejemplos de uso del cliente Chatterbox TTS en español")
    print("=" * 70)
    
    # Ejemplo 1: Generación básica
    print("\n📝 Ejemplo 1: Generación básica")
    cliente.generar(
        texto="Hola, bienvenido al sistema de síntesis de voz en español.",
        archivo_salida="audios/ejemplo1_basico.wav"
    )
    
    # Ejemplo 2: Con más expresividad
    print("\n📝 Ejemplo 2: Voz más expresiva")
    cliente.generar(
        texto="¡Esto es increíble! La tecnología de síntesis de voz ha avanzado muchísimo.",
        expresividad=1.0,
        temperatura=0.9,
        archivo_salida="audios/ejemplo2_expresivo.wav"
    )
    
    # Ejemplo 3: Voz más neutral
    print("\n📝 Ejemplo 3: Voz neutral y profesional")
    cliente.generar(
        texto="En el siguiente informe se presentan los resultados del análisis realizado durante el último trimestre.",
        expresividad=0.4,
        temperatura=0.7,
        archivo_salida="audios/ejemplo3_neutral.wav"
    )
    
    # Ejemplo 4: Con audio de referencia (si existe)
    print("\n📝 Ejemplo 4: Con audio de referencia")
    audio_ref = "voz_referencia.wav"
    if os.path.exists(audio_ref):
        cliente.generar(
            texto="Este audio usará las características de la voz de referencia.",
            audio_referencia=audio_ref,
            archivo_salida="audios/ejemplo4_clonado.wav"
        )
    else:
        print(f"   ⚠️  Archivo {audio_ref} no encontrado, saltando ejemplo")
    
    # Ejemplo 5: Múltiples textos
    print("\n📝 Ejemplo 5: Generación de múltiples audios")
    textos = [
        "Buenos días, ¿cómo estás?",
        "El clima hoy está muy agradable.",
        "Gracias por tu atención.",
        "Hasta luego, que tengas un excelente día.",
    ]
    
    resultados = cliente.generar_varios(
        textos=textos,
        carpeta_salida="audios/varios",
        expresividad=0.6
    )
    
    # Resumen
    print("\n" + "=" * 70)
    print("✅ Ejemplos completados")
    print("=" * 70)
    exitosos = sum(1 for r in resultados if "error" not in r)
    print(f"Generaciones exitosas: {exitosos}/{len(resultados)}")
    print(f"Archivos guardados en: audios/")


if __name__ == "__main__":
    main()
        """
        Generar audio TTS.
        
        Args:
            text: Texto a sintetizar (máximo 300 caracteres)
            language_id: Código de idioma (en, es, fr, etc.)
            audio_prompt_path: Ruta al archivo de audio de referencia (opcional)
            exaggeration: Control de expresividad (0.25-2.0)
            temperature: Control de aleatoriedad (0.05-5.0)
            cfg_weight: Peso CFG/Pace (0.2-1.0)
            seed: Semilla aleatoria (0 para aleatorio)
            output_path: Ruta donde guardar el audio generado
        
        Returns:
            Diccionario con información de la respuesta
        """
        # Preparar payload
        payload = {
            "inputs": text[:300],  # Truncar a 300 caracteres
            "parameters": {
                "language_id": language_id,
                "exaggeration": exaggeration,
                "temperature": temperature,
                "cfg_weight": cfg_weight,
                "seed": seed,
                "return_format": "base64"
            }
        }
        
        # Agregar audio de referencia si se proporciona
        if audio_prompt_path and os.path.exists(audio_prompt_path):
            with open(audio_prompt_path, "rb") as f:
                audio_bytes = f.read()
                audio_base64 = base64.b64encode(audio_bytes).decode('utf-8')
                payload["parameters"]["audio_prompt_base64"] = audio_base64
        
        # Hacer request
        try:
            response = requests.post(
                self.endpoint_url,
                headers=self.headers,
                json=payload,
                timeout=60
            )
            response.raise_for_status()
            result = response.json()
            
            # Verificar si hay error
            if "error" in result:
                print(f"❌ Error del servidor: {result['error']}")
                return result
            
            # Decodificar y guardar audio
            if "audio" in result:
                audio_data = base64.b64decode(result["audio"])
                
                # Crear directorio si no existe
                output_dir = Path(output_path).parent
                if output_dir != Path('.'):
                    output_dir.mkdir(parents=True, exist_ok=True)
                
                with open(output_path, "wb") as f:
                    f.write(audio_data)
                
                print(f"✅ Audio generado exitosamente:")
                print(f"   - Archivo: {output_path}")
                print(f"   - Sample rate: {result['sample_rate']} Hz")
                print(f"   - Idioma: {result['language']}")
                print(f"   - Texto: {result['text']}")
                
                result["output_path"] = output_path
            
            return result
            
        except requests.exceptions.Timeout:
            print("❌ Error: Request timeout (>60s)")
            return {"error": "Request timeout"}
        except requests.exceptions.RequestException as e:
            print(f"❌ Error en el request: {str(e)}")
            return {"error": str(e)}
        except Exception as e:
            print(f"❌ Error inesperado: {str(e)}")
            return {"error": str(e)}
    
    def batch_generate(
        self,
        texts_and_languages: list[tuple[str, str]],
        output_dir: str = "outputs",
        **kwargs
    ) -> list[dict]:
        """
        Generar múltiples audios en batch.
        
        Args:
            texts_and_languages: Lista de tuplas (texto, language_id)
            output_dir: Directorio donde guardar los audios
            **kwargs: Parámetros adicionales para generate()
        
        Returns:
            Lista de diccionarios con resultados
        """
        results = []
        
        # Crear directorio de salida
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        
        for i, (text, lang) in enumerate(texts_and_languages):
            print(f"\n[{i+1}/{len(texts_and_languages)}] Generando: {text[:50]}...")
            
            output_path = os.path.join(output_dir, f"output_{i+1}_{lang}.wav")
            result = self.generate(
                text=text,
                language_id=lang,
                output_path=output_path,
                **kwargs
            )
            results.append(result)
        
        return results


def main():
    """Ejemplos de uso del cliente."""
    
    # ⚠️ CONFIGURACIÓN - Reemplaza con tus valores
    ENDPOINT_URL = "https://your-endpoint.endpoints.huggingface.cloud"
    HF_TOKEN = os.getenv("HF_TOKEN", "your_token_here")
    
    # Verificar configuración
    if "your-endpoint" in ENDPOINT_URL or "your_token" in HF_TOKEN:
        print("⚠️  ADVERTENCIA: Debes configurar ENDPOINT_URL y HF_TOKEN")
        print("   Edita este archivo o configura la variable de entorno HF_TOKEN")
        return
    
    # Crear cliente
    client = ChatterboxTTSClient(ENDPOINT_URL, HF_TOKEN)
    
    print("=" * 70)
    print("Ejemplos de uso del cliente Chatterbox Multilingual TTS")
    print("=" * 70)
    
    # Ejemplo 1: Generación básica
    print("\n📝 Ejemplo 1: Generación básica en español")
    client.generate(
        text="Hola, este es un ejemplo de síntesis de voz en español.",
        language_id="es",
        output_path="outputs/ejemplo1_es.wav"
    )
    
    # Ejemplo 2: Con parámetros personalizados
    print("\n📝 Ejemplo 2: Con expresividad alta")
    client.generate(
        text="¡Esto es increíble! La tecnología de síntesis de voz es asombrosa.",
        language_id="es",
        exaggeration=1.2,
        temperature=0.9,
        output_path="outputs/ejemplo2_expresivo.wav"
    )
    
    # Ejemplo 3: Con audio de referencia (si existe)
    print("\n📝 Ejemplo 3: Con audio de referencia")
    reference_audio = "reference_voice.wav"
    if os.path.exists(reference_audio):
        client.generate(
            text="Este audio usará la voz del archivo de referencia.",
            language_id="es",
            audio_prompt_path=reference_audio,
            output_path="outputs/ejemplo3_clonado.wav"
        )
    else:
        print(f"   ⚠️  Archivo {reference_audio} no encontrado, saltando ejemplo")
    
    # Ejemplo 4: Múltiples idiomas
    print("\n📝 Ejemplo 4: Generación en múltiples idiomas")
    texts_and_langs = [
        ("Hello, this is a test in English.", "en"),
        ("Bonjour, ceci est un test en français.", "fr"),
        ("Hallo, das ist ein Test auf Deutsch.", "de"),
        ("Ciao, questo è un test in italiano.", "it"),
    ]
    
    results = client.batch_generate(
        texts_and_languages=texts_and_langs,
        output_dir="outputs/multilingual",
        exaggeration=0.5,
        temperature=0.8
    )
    
    # Resumen
    print("\n" + "=" * 70)
    print("✅ Ejemplos completados")
    print("=" * 70)
    successful = sum(1 for r in results if "error" not in r)
    print(f"Generaciones exitosas: {successful}/{len(results)}")
    print(f"Archivos guardados en: outputs/")


if __name__ == "__main__":
    main()
