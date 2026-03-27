# 💡 Ejemplos Prácticos de Uso

Casos de uso reales para el sistema de síntesis de voz en español.

## 📱 Asistente Virtual

```python
from example_client import ChatterboxTTSClient

cliente = ChatterboxTTSClient(ENDPOINT_URL, TOKEN)

# Respuestas del asistente
respuestas = [
    "Hola, ¿en qué puedo ayudarte hoy?",
    "He encontrado tres opciones que podrían interesarte.",
    "Perfecto, he completado tu solicitud.",
    "¿Hay algo más en lo que pueda asistirte?"
]

for i, respuesta in enumerate(respuestas):
    cliente.generar(
        texto=respuesta,
        expresividad=0.6,  # Natural y amigable
        archivo_salida=f"asistente/respuesta_{i+1}.wav"
    )
```

## 📰 Narración de Noticias

```python
# Voz neutral y profesional para noticias
noticia = """
Buenos días. En las noticias de hoy, el gobierno anunció nuevas medidas 
económicas que entrarán en vigor el próximo mes. Los expertos consideran 
que estas medidas tendrán un impacto positivo en la economía nacional.
"""

cliente.generar(
    texto=noticia,
    expresividad=0.4,  # Neutral y profesional
    temperatura=0.7,   # Consistente
    archivo_salida="noticias/noticia_hoy.wav"
)
```

## 🎓 Contenido Educativo

```python
# Lección educativa con tono claro
leccion = """
Hoy aprenderemos sobre el ciclo del agua. El agua se evapora de los océanos, 
forma nubes en la atmósfera, y luego cae como lluvia. Este proceso se repite 
constantemente y es fundamental para la vida en nuestro planeta.
"""

cliente.generar(
    texto=leccion,
    expresividad=0.6,  # Claro y didáctico
    temperatura=0.8,
    archivo_salida="educacion/leccion_agua.wav"
)
```

## 📢 Publicidad y Marketing

```python
# Anuncio publicitario con energía
anuncio = """
¡Increíble oferta por tiempo limitado! Obtén hasta un cincuenta por ciento 
de descuento en todos nuestros productos. No dejes pasar esta oportunidad única. 
¡Visítanos hoy mismo!
"""

cliente.generar(
    texto=anuncio,
    expresividad=1.0,  # Muy expresivo y energético
    temperatura=0.9,
    archivo_salida="marketing/anuncio_oferta.wav"
)
```

## 📖 Audiolibros y Narración

```python
# Narración de historia con emoción
historia = """
Era una noche oscura y tormentosa. María caminaba por el bosque cuando 
escuchó un ruido extraño entre los árboles. Su corazón comenzó a latir 
más rápido mientras se acercaba cautelosamente al origen del sonido.
"""

cliente.generar(
    texto=historia,
    expresividad=0.8,  # Narrativo con emoción
    temperatura=0.85,
    archivo_salida="audiolibros/capitulo_1.wav"
)
```

## 🏢 Mensajes Corporativos

```python
# Mensaje de bienvenida corporativo
bienvenida = """
Bienvenido a nuestra empresa. Estamos comprometidos con la excelencia 
y la innovación. Nuestro equipo está aquí para ayudarte a alcanzar 
tus objetivos. Gracias por confiar en nosotros.
"""

cliente.generar(
    texto=bienvenida,
    expresividad=0.5,  # Profesional y cálido
    temperatura=0.75,
    archivo_salida="corporativo/bienvenida.wav"
)
```

## 🎮 Videojuegos - Personajes

```python
# Diferentes personajes con diferentes estilos

# Personaje heroico
cliente.generar(
    texto="¡No te preocupes! Yo me encargaré de esto.",
    expresividad=0.9,
    archivo_salida="juego/heroe_1.wav"
)

# Personaje sabio
cliente.generar(
    texto="La sabiduría viene con la experiencia, joven aventurero.",
    expresividad=0.4,
    temperatura=0.7,
    archivo_salida="juego/sabio_1.wav"
)

# Personaje emocionado
cliente.generar(
    texto="¡Wow! ¡Esto es increíble! ¡Mira lo que encontré!",
    expresividad=1.2,
    temperatura=0.95,
    archivo_salida="juego/emocionado_1.wav"
)
```

## 📞 Sistema IVR (Respuesta de Voz Interactiva)

```python
# Menú telefónico
mensajes_ivr = {
    "bienvenida": "Gracias por llamar. Por favor, escuche las siguientes opciones.",
    "opcion_1": "Para ventas, presione uno.",
    "opcion_2": "Para soporte técnico, presione dos.",
    "opcion_3": "Para hablar con un operador, presione cero.",
    "despedida": "Gracias por su llamada. Que tenga un excelente día."
}

for nombre, texto in mensajes_ivr.items():
    cliente.generar(
        texto=texto,
        expresividad=0.5,
        temperatura=0.7,
        archivo_salida=f"ivr/{nombre}.wav"
    )
```

## 🚗 Navegación GPS

```python
# Instrucciones de navegación
instrucciones = [
    "En doscientos metros, gire a la derecha.",
    "Continúe recto por quinientos metros.",
    "Ha llegado a su destino.",
    "Recalculando ruta."
]

for i, instruccion in enumerate(instrucciones):
    cliente.generar(
        texto=instruccion,
        expresividad=0.4,  # Clara y directa
        temperatura=0.6,
        archivo_salida=f"gps/instruccion_{i+1}.wav"
    )
```

## 🏥 Aplicaciones de Salud

```python
# Recordatorios médicos
recordatorios = [
    "Es hora de tomar tu medicamento.",
    "Recuerda beber agua regularmente.",
    "No olvides tu cita médica mañana a las diez de la mañana.",
    "Excelente trabajo completando tu rutina de ejercicios."
]

for i, recordatorio in enumerate(recordatorios):
    cliente.generar(
        texto=recordatorio,
        expresividad=0.6,  # Amable y motivador
        archivo_salida=f"salud/recordatorio_{i+1}.wav"
    )
```

## 🎵 Podcasts

```python
# Introducción de podcast
intro = """
Bienvenidos a un nuevo episodio de nuestro podcast. Hoy hablaremos sobre 
las últimas tendencias en tecnología y cómo están transformando nuestra 
vida cotidiana. Soy tu anfitrión y estoy emocionado de compartir este 
contenido contigo.
"""

cliente.generar(
    texto=intro,
    expresividad=0.7,  # Conversacional y entusiasta
    temperatura=0.85,
    archivo_salida="podcast/intro_episodio_5.wav"
)
```

## 🛍️ E-commerce

```python
# Confirmaciones de compra
confirmaciones = [
    "Tu pedido ha sido confirmado exitosamente.",
    "Tu paquete está en camino y llegará en dos días hábiles.",
    "Tu compra ha sido procesada. Recibirás un correo de confirmación.",
    "Gracias por tu compra. Esperamos que disfrutes tu producto."
]

for i, confirmacion in enumerate(confirmaciones):
    cliente.generar(
        texto=confirmacion,
        expresividad=0.6,
        archivo_salida=f"ecommerce/confirmacion_{i+1}.wav"
    )
```

## 🎬 Producción de Video

```python
# Narración para video corporativo
narracion_video = """
En nuestra empresa, creemos en el poder de la innovación. Cada día trabajamos 
para crear soluciones que mejoren la vida de nuestros clientes. Con más de 
veinte años de experiencia, somos líderes en nuestro sector.
"""

cliente.generar(
    texto=narracion_video,
    expresividad=0.6,
    temperatura=0.8,
    archivo_salida="video/narracion_corporativa.wav"
)
```

## 🔄 Generación en Lote

```python
# Generar múltiples audios de una vez
textos_batch = [
    "Mensaje uno: Bienvenido al sistema.",
    "Mensaje dos: Tu solicitud ha sido procesada.",
    "Mensaje tres: Operación completada exitosamente.",
    "Mensaje cuatro: Gracias por usar nuestro servicio.",
    "Mensaje cinco: Hasta pronto."
]

resultados = cliente.generar_varios(
    textos=textos_batch,
    carpeta_salida="batch_output",
    expresividad=0.6
)

print(f"✅ Generados {len(resultados)} audios")
```

## 🎯 Consejos por Tipo de Contenido

### Contenido Formal (Noticias, Corporativo)
```python
expresividad=0.3-0.5
temperatura=0.6-0.7
```

### Contenido Conversacional (Asistentes, Tutoriales)
```python
expresividad=0.5-0.7
temperatura=0.8-0.85
```

### Contenido Expresivo (Marketing, Entretenimiento)
```python
expresividad=0.8-1.2
temperatura=0.85-0.95
```

### Contenido Narrativo (Audiolibros, Podcasts)
```python
expresividad=0.6-0.8
temperatura=0.8-0.9
```

## 🎨 Personalización Avanzada

### Voz Rápida y Dinámica
```python
cliente.generar(
    texto="¡Rápido! ¡No hay tiempo que perder!",
    expresividad=1.0,
    temperatura=0.9,
    peso_cfg=0.3  # Más rápido
)
```

### Voz Lenta y Reflexiva
```python
cliente.generar(
    texto="Reflexionemos sobre este importante tema.",
    expresividad=0.4,
    temperatura=0.7,
    peso_cfg=0.7  # Más lento
)
```

## 📝 Notas Importantes

1. **Longitud del texto**: Máximo 300 caracteres por solicitud
2. **Puntuación**: Usa puntos, comas y signos de exclamación para mejor entonación
3. **Números**: Escribe números en palabras para mejor pronunciación
4. **Abreviaturas**: Evita abreviaturas, escribe las palabras completas

## 🚀 Optimización

Para mejor rendimiento:
- Genera audios en lote cuando sea posible
- Reutiliza audios comunes (saludos, despedidas)
- Cachea respuestas frecuentes
- Usa semillas fijas para reproducibilidad

---

¿Necesitas más ejemplos? Revisa `example_client.py` para ver el código completo.
