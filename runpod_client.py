"""
Cliente optimizado para consumir Chatterbox TTS en RunPod
"""

import requests
import base64
import os
from pathlib import Path
from typing import Optional
import time


class ChatterboxRunPodClient:
    """Cliente para interactuar con Chatterbox TTS deployado en RunPod."""
    
    def __init__(self, endpoint_id: str, api_key: str):
        """
        Inicializar el cliente.
        
        Args:
            endpoint_id: ID del endpoint de RunPod
            api_key: API key de RunPod
        """
        self.endpoint_url = f"https://api.runpod.ai/v2/{endpoint_id}/runsync"
        self.api_key = api_key
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
    
    def generar(
        self,
        texto: str,
        expresividad: float = 0.6,
        temperatura: float = 0.85,
        peso_cfg: float = 0.5,
        semilla: int = 0,
        archivo_salida: str = "voz.wav",
        timeout: int = 60
    ) -> dict:
        """
        Generar audio de voz en español.
        
        Args:
            texto: Texto a sintetizar (máximo 300 caracteres)
            expresividad: Control de expresividad (0.25-2.0)
            temperatura: Control de variabilidad (0.05-5.0)
            peso_cfg: Peso de control de ritmo (0.2-1.0)
            semilla: Semilla aleatoria (0 para aleatorio)
            archivo_salida: Ruta donde guardar el audio
            timeout: Timeout en segundos
        
        Returns:
            Diccionario con información de la respuesta
        """
        payload = {
            "input": {
                "texto": texto[:300],
                "exaggeration": expresividad,
                "temperature": temperatura,
                "cfg_weight": peso_cfg,
                "seed": semilla
            }
        }
        
        try:
            print(f"📤 Enviando solicitud: '{texto[:50]}...'")
            start_time = time.time()
            
            response = requests.post(
                self.endpoint_url,
                headers=self.headers,
                json=payload,
                timeout=timeout
            )
            response.raise_for_status()
            result = response.json()
            
            elapsed = time.time() - start_time
            
            # Verificar errores
            if "error" in result:
                print(f"❌ Error del servidor: {result['error']}")
                return result
            
            # Extraer audio
            if "output" in result and "audio" in result["output"]:
                audio_base64 = result["output"]["audio"]
                audio_data = base64.b64decode(audio_base64)
                
                # Crear directorio si no existe
                output_dir = Path(archivo_salida).parent
                if output_dir != Path('.'):
                    output_dir.mkdir(parents=True, exist_ok=True)
                
                # Guardar audio
                with open(archivo_salida, "wb") as f:
                    f.write(audio_data)
                
                print(f"✅ Audio generado en {elapsed:.2f}s")
                print(f"   - Archivo: {archivo_salida}")
                print(f"   - Frecuencia: {result['output'].get('sample_rate', 24000)} Hz")
                print(f"   - Texto: {result['output'].get('text', texto)}")
                
                result["output"]["archivo_salida"] = archivo_salida
                result["output"]["tiempo_generacion"] = elapsed
                
                return result["output"]
            else:
                print("❌ Respuesta sin audio")
                return {"error": "Respuesta inválida del servidor"}
            
        except requests.exceptions.Timeout:
            print(f"❌ Timeout: El servidor tardó más de {timeout}s")
            return {"error": "Timeout del servidor"}
        except requests.exceptions.RequestException as e:
            print(f"❌ Error de conexión: {str(e)}")
            return {"error": str(e)}
        except Exception as e:
            print(f"❌ Error inesperado: {str(e)}")
            return {"error": str(e)}
    
    def generar_varios(
        self,
        textos: list[str],
        carpeta_salida: str = "audios_runpod",
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
        
        # Crear carpeta
        Path(carpeta_salida).mkdir(parents=True, exist_ok=True)
        
        print(f"\n🎙️ Generando {len(textos)} audios...")
        
        for i, texto in enumerate(textos, 1):
            print(f"\n[{i}/{len(textos)}]")
            
            archivo_salida = os.path.join(carpeta_salida, f"audio_{i}.wav")
            resultado = self.generar(
                texto=texto,
                archivo_salida=archivo_salida,
                **kwargs
            )
            resultados.append(resultado)
        
        exitosos = sum(1 for r in resultados if "error" not in r)
        print(f"\n✅ Completado: {exitosos}/{len(textos)} exitosos")
        
        return resultados
    
    def health_check(self) -> bool:
        """
        Verificar si el endpoint está funcionando.
        
        Returns:
            True si el endpoint responde correctamente
        """
        try:
            resultado = self.generar(
                texto="Prueba de conexión",
                archivo_salida="/tmp/test.wav"
            )
            
            if "error" not in resultado:
                print("✅ Endpoint funcionando correctamente")
                # Limpiar archivo de prueba
                if os.path.exists("/tmp/test.wav"):
                    os.remove("/tmp/test.wav")
                return True
            else:
                print(f"❌ Endpoint con errores: {resultado['error']}")
                return False
                
        except Exception as e:
            print(f"❌ Endpoint no disponible: {str(e)}")
            return False


def main():
    """Ejemplos de uso del cliente RunPod."""
    
    # ⚠️ CONFIGURACIÓN - Reemplaza con tus valores
    ENDPOINT_ID = "tu_endpoint_id"  # Ej: "abc123def456"
    API_KEY = os.getenv("RUNPOD_API_KEY", "tu_api_key")
    
    # Verificar configuración
    if "tu_endpoint" in ENDPOINT_ID or "tu_api" in API_KEY:
        print("⚠️  ADVERTENCIA: Debes configurar ENDPOINT_ID y API_KEY")
        print("   Edita este archivo o configura la variable RUNPOD_API_KEY")
        return
    
    # Crear cliente
    cliente = ChatterboxRunPodClient(ENDPOINT_ID, API_KEY)
    
    print("=" * 70)
    print("Cliente RunPod - Chatterbox TTS en Español")
    print("=" * 70)
    
    # Health check
    print("\n🔍 Verificando endpoint...")
    if not cliente.health_check():
        print("❌ El endpoint no está disponible. Verifica la configuración.")
        return
    
    # Ejemplo 1: Generación básica
    print("\n📝 Ejemplo 1: Generación básica")
    cliente.generar(
        texto="Hola, bienvenido al sistema de síntesis de voz en español.",
        archivo_salida="ejemplos_runpod/ejemplo1.wav"
    )
    
    # Ejemplo 2: Voz expresiva
    print("\n📝 Ejemplo 2: Voz expresiva")
    cliente.generar(
        texto="¡Esto es increíble! La tecnología de voz es asombrosa.",
        expresividad=1.0,
        temperatura=0.9,
        archivo_salida="ejemplos_runpod/ejemplo2_expresivo.wav"
    )
    
    # Ejemplo 3: Voz neutral
    print("\n📝 Ejemplo 3: Voz neutral y profesional")
    cliente.generar(
        texto="En el siguiente informe se presentan los resultados del análisis.",
        expresividad=0.4,
        temperatura=0.7,
        archivo_salida="ejemplos_runpod/ejemplo3_neutral.wav"
    )
    
    # Ejemplo 4: Múltiples audios
    print("\n📝 Ejemplo 4: Generación en lote")
    textos = [
        "Buenos días, ¿cómo estás?",
        "El clima hoy está muy agradable.",
        "Gracias por tu atención.",
        "Hasta luego, que tengas un excelente día."
    ]
    
    resultados = cliente.generar_varios(
        textos=textos,
        carpeta_salida="ejemplos_runpod/lote",
        expresividad=0.6
    )
    
    # Resumen
    print("\n" + "=" * 70)
    print("✅ Ejemplos completados")
    print("=" * 70)
    print(f"Archivos guardados en: ejemplos_runpod/")


if __name__ == "__main__":
    main()
