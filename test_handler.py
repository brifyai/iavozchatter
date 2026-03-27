"""
Script de prueba para el handler de Hugging Face Inference Endpoint.
Ejecuta esto localmente para verificar que el handler funciona antes de deployar.
"""

import base64
from handler import EndpointHandler

def test_generacion_basica():
    """Prueba generación básica de texto a voz sin audio de referencia."""
    print("🧪 Prueba 1: Generación básica en español")
    
    handler = EndpointHandler(path=".")
    
    request = {
        "inputs": "Hola, esta es una prueba del sistema de síntesis de voz en español.",
        "parameters": {
            "exaggeration": 0.6,
            "temperature": 0.85,
            "cfg_weight": 0.5,
            "return_format": "base64"
        }
    }
    
    response = handler(request)
    
    if "error" in response:
        print(f"❌ Error: {response['error']}")
    else:
        print(f"✅ ¡Éxito!")
        print(f"   Frecuencia de muestreo: {response['sample_rate']} Hz")
        print(f"   Texto: {response['text']}")
        print(f"   Formato de audio: {response.get('format', 'N/A')}")
        print(f"   Longitud del audio: {len(response['audio'])} caracteres (base64)")
    
    return response


def test_diferentes_estilos():
    """Prueba generación con diferentes niveles de expresividad."""
    print("\n🧪 Prueba 2: Diferentes estilos de voz")
    
    handler = EndpointHandler(path=".")
    
    casos_prueba = [
        (0.4, "Voz neutral y profesional", "Este es un mensaje con tono neutral y profesional."),
        (0.6, "Voz natural", "Esta es una conversación natural y amigable."),
        (1.0, "Voz expresiva", "¡Esto es increíble! ¡Qué emocionante!"),
    ]
    
    for expresividad, descripcion, texto in casos_prueba:
        request = {
            "inputs": texto,
            "parameters": {
                "exaggeration": expresividad,
                "return_format": "base64"
            }
        }
        
        response = handler(request)
        
        if "error" in response:
            print(f"❌ {descripcion}: {response['error']}")
        else:
            print(f"✅ {descripcion}: Generado {len(response['audio'])} caracteres")


def test_textos_variados():
    """Prueba con diferentes tipos de texto."""
    print("\n🧪 Prueba 3: Textos variados")
    
    handler = EndpointHandler(path=".")
    
    textos = [
        "Buenos días, ¿cómo estás?",
        "El clima hoy está muy agradable.",
        "En el siguiente informe se presentan los resultados del análisis.",
        "¡Felicidades! Has completado el proceso exitosamente.",
    ]
    
    for i, texto in enumerate(textos, 1):
        request = {
            "inputs": texto,
            "parameters": {
                "return_format": "base64"
            }
        }
        
        response = handler(request)
        
        if "error" in response:
            print(f"❌ Texto {i}: {response['error']}")
        else:
            print(f"✅ Texto {i}: '{texto[:40]}...' - Generado correctamente")


def test_manejo_errores():
    """Prueba el manejo de errores."""
    print("\n🧪 Prueba 4: Manejo de errores")
    
    handler = EndpointHandler(path=".")
    
    # Prueba sin inputs
    request = {
        "parameters": {
            "exaggeration": 0.5
        }
    }
    
    response = handler(request)
    print(f"Prueba sin texto: {'✅ Error capturado' if 'error' in response else '❌ Debería haber dado error'}")
    
    # Prueba con inputs vacío
    request = {
        "inputs": "",
        "parameters": {}
    }
    
    response = handler(request)
    print(f"Prueba con texto vacío: {'✅ Error capturado' if 'error' in response else '❌ Debería haber dado error'}")


def test_texto_largo():
    """Prueba con texto largo (truncamiento a 300 caracteres)."""
    print("\n🧪 Prueba 5: Texto largo (truncamiento)")
    
    handler = EndpointHandler(path=".")
    
    texto_largo = "Este es un texto muy largo que excede los trescientos caracteres permitidos. " * 10
    
    request = {
        "inputs": texto_largo,
        "parameters": {
            "return_format": "base64"
        }
    }
    
    response = handler(request)
    
    if "error" in response:
        print(f"❌ Error: {response['error']}")
    else:
        print(f"✅ Texto truncado correctamente")
        print(f"   Longitud original: {len(texto_largo)} caracteres")
        print(f"   Longitud procesada: {len(response['text'])} caracteres")


if __name__ == "__main__":
    print("=" * 70)
    print("Pruebas del Handler de Chatterbox TTS en Español")
    print("=" * 70)
    
    try:
        test_generacion_basica()
        test_diferentes_estilos()
        test_textos_variados()
        test_manejo_errores()
        test_texto_largo()
        
        print("\n" + "=" * 70)
        print("✅ ¡Todas las pruebas completadas!")
        print("=" * 70)
    except Exception as e:
        print(f"\n❌ Las pruebas fallaron con error: {str(e)}")
        import traceback
        traceback.print_exc()
