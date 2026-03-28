"""
Cliente para consumir Chatterbox TTS en RunPod Pod (HTTP)
"""

import requests
import base64
import os
from pathlib import Path


class ChatterboxPodClient:
    """Cliente para interactuar con Chatterbox TTS en RunPod Pod."""
    
    def __init__(self, pod_url: str):
        """
        Inicializar el cliente.
        
        Args:
            pod_url: URL del pod (ej: https://gzoh7jg9n9o7rk-8000.proxy.runpod.net)
        """
        self.pod_url = pod_url.rstrip('/')
    
    def health_check(self) -> bool:
        """Verificar si el servidor está funcionando."""
        try:
            response = requests.get(f"{self.pod_url}/health", timeout=5)
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Servidor funcionando")
                print(f"   - Estado: {data.get('status')}")
                print(f"   - Modelo cargado: {data.get('model_loaded')}")
                print(f"   - Dispositivo: {data.get('device')}")
                return True
            return False
        except Exception as e:
            print(f"❌ Error: {str(e)}")
            return False
    
    def generar(
        self,
        texto: str,
        expresividad: float = 0.6,
        temperatura: float = 0.85,
        peso_cfg: float = 0.5,
        semilla: int = 0,
        archivo_salida: str = "voz.wav"
    ) -> dict:
        """
        Generar audio de voz en español.
        
        Args:
            texto: Texto a sintetizar
            expresividad: Control de expresividad (0.25-2.0)
            temperatura: Control de variabilidad (0.05-5.0)
            peso_cfg: Peso de control de ritmo (0.2-1.0)
            semilla: Semilla aleatoria (0 para aleatorio)
            archivo_salida: Ruta donde guardar el audio
        
        Returns:
            Diccionario con información de la respuesta
        """
        try:
            print(f"📤 Enviando: '{texto[:50]}...'")
            
            response = requests.post(
                f"{self.pod_url}/generate",
                json={
                    "texto": texto,
                    "exaggeration": expresividad,
                    "temperature": temperatura,
                    "cfg_weight": peso_cfg,
                    "seed": semilla
                },
                timeout=60
            )
            
            response.raise_for_status()
            result = response.json()
            
            # Decodificar audio
            audio_base64 = result["audio"]
            audio_data = base64.b64decode(audio_base64)
            
            # Crear directorio si no existe
            output_dir = Path(archivo_salida).parent
            if output_dir != Path('.'):
                output_dir.mkdir(parents=True, exist_ok=True)
            
            # Guardar audio
            with open(archivo_salida, "wb") as f:
                f.write(audio_data)
            
            print(f"✅ Audio generado: {archivo_salida}")
            print(f"   - Frecuencia: {result['sample_rate']} Hz")
            print(f"   - Texto: {result['text']}")
            
            return result
            
        except requests.exceptions.Timeout:
            print("❌ Timeout: El servidor tardó más de 60s")
            return {"error": "Timeout"}
        except requests.exceptions.RequestException as e:
            print(f"❌ Error de conexión: {str(e)}")
            return {"error": str(e)}
        except Exception as e:
            print(f"❌ Error: {str(e)}")
            return {"error": str(e)}


def main():
    """Ejemplo de uso"""
    
    # ⚠️ Reemplaza con la URL de tu Pod
    POD_URL = "https://gzoh7jg9n9o7rk-8000.proxy.runpod.net"
    
    cliente = ChatterboxPodClient(POD_URL)
    
    print("=" * 70)
    print("Cliente RunPod Pod - Chatterbox TTS")
    print("=" * 70)
    
    # Health check
    print("\n🔍 Verificando servidor...")
    if not cliente.health_check():
        print("❌ El servidor no está disponible")
        return
    
    # Generar audio
    print("\n📝 Generando audio...")
    cliente.generar(
        texto="Hola, bienvenido al sistema de síntesis de voz en español.",
        archivo_salida="prueba_pod.wav"
    )


if __name__ == "__main__":
    main()
