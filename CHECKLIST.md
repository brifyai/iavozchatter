# ✅ Checklist de Deployment - Hugging Face Inference Endpoints

Usa este checklist para asegurarte de que todo está listo antes y después del deployment.

## 📦 Pre-Deployment

### Archivos Requeridos en el Repositorio

- [ ] `handler.py` está en la raíz del repositorio
- [ ] `requirements.txt` incluye todas las dependencias (incluyendo `soundfile`)
- [ ] `src/chatterbox/` carpeta completa con todo el código fuente
- [ ] `ve.pt` - Voice Encoder weights
- [ ] `t3_mtl23ls_v2.safetensors` - T3 model weights
- [ ] `s3gen.pt` - S3Gen model weights
- [ ] `grapheme_mtl_merged_expanded_v1.json` - Tokenizer
- [ ] `conds.pt` - Default conditionals
- [ ] `Cangjie5_TC.json` - Para soporte de chino (opcional pero recomendado)

### Verificación del Handler

- [ ] La clase `EndpointHandler` está definida en `handler.py`
- [ ] Método `__init__(self, path="")` implementado
- [ ] Método `__call__(self, data: Dict[str, Any])` implementado
- [ ] Manejo de errores implementado
- [ ] Validación de parámetros implementada

### Testing Local

- [ ] Ejecutar `python test_handler.py` sin errores
- [ ] Test de generación básica funciona
- [ ] Test de múltiples idiomas funciona
- [ ] Test de manejo de errores funciona

### Configuración de Hugging Face

- [ ] Cuenta de Hugging Face creada
- [ ] Token de acceso con permisos de escritura generado
- [ ] Repositorio del modelo creado en Hugging Face Hub
- [ ] Todos los archivos subidos al repositorio

## 🚀 Durante el Deployment

### Configuración del Endpoint

- [ ] Nombre del endpoint definido (ej: `chatterbox-multilingual-tts`)
- [ ] Repositorio correcto seleccionado
- [ ] Task detectado como "Custom"
- [ ] Cloud provider seleccionado (AWS/Azure/GCP)
- [ ] Región seleccionada (cercana a usuarios)
- [ ] Tipo de instancia seleccionado:
  - [ ] Mínimo: GPU [medium] - 1x Nvidia A10G
  - [ ] Recomendado: GPU [xlarge] - 1x Nvidia A100
- [ ] Scaling configurado:
  - [ ] Min replicas: 1
  - [ ] Max replicas: según necesidad
- [ ] Variables de entorno configuradas (si necesario)

### Monitoreo del Deployment

- [ ] Estado cambia de `initializing` a `pending`
- [ ] Logs muestran descarga de modelo
- [ ] Logs muestran instalación de dependencias
- [ ] Logs muestran "Model loaded successfully"
- [ ] Estado cambia a `running`
- [ ] URL del endpoint disponible

## ✅ Post-Deployment

### Verificación Básica

- [ ] Endpoint en estado `running`
- [ ] URL del endpoint accesible
- [ ] Test básico con cURL funciona
- [ ] Test con Python client funciona

### Tests Funcionales

- [ ] Generación en inglés funciona
- [ ] Generación en español funciona
- [ ] Generación en francés funciona
- [ ] Al menos 3 idiomas diferentes probados
- [ ] Generación con audio de referencia funciona (opcional)
- [ ] Parámetros personalizados funcionan (exaggeration, temperature)
- [ ] Manejo de errores funciona correctamente

### Performance

- [ ] Latencia < 10 segundos para textos cortos
- [ ] Latencia < 30 segundos para textos largos (300 chars)
- [ ] GPU utilization > 50% durante generación
- [ ] No hay errores de memoria (OOM)

### Seguridad

- [ ] Autenticación con token funciona
- [ ] Requests sin token son rechazados
- [ ] Rate limiting configurado (si necesario)
- [ ] Logs de acceso habilitados

## 📊 Monitoreo Continuo

### Métricas a Vigilar

- [ ] Latencia promedio
- [ ] Throughput (requests/segundo)
- [ ] Error rate (%)
- [ ] GPU utilization (%)
- [ ] Costos acumulados

### Alertas Configuradas

- [ ] Alerta si error rate > 5%
- [ ] Alerta si latencia > 60 segundos
- [ ] Alerta si endpoint está down
- [ ] Alerta si costos exceden presupuesto

## 📚 Documentación

### Para el Equipo

- [ ] URL del endpoint compartida
- [ ] Token de acceso compartido (de forma segura)
- [ ] Documentación de uso compartida ([ENDPOINT_USAGE.md](./ENDPOINT_USAGE.md))
- [ ] Ejemplos de código compartidos ([example_client.py](./example_client.py))
- [ ] Idiomas soportados documentados
- [ ] Límites y restricciones documentados

### Para Usuarios

- [ ] README actualizado con información del endpoint
- [ ] Ejemplos de uso publicados
- [ ] Guía de troubleshooting disponible
- [ ] Contacto de soporte definido

## 🔄 Mantenimiento

### Actualizaciones

- [ ] Proceso de actualización documentado
- [ ] Estrategia de rollback definida
- [ ] Ventana de mantenimiento comunicada

### Backup

- [ ] Archivos del modelo respaldados
- [ ] Configuración del endpoint documentada
- [ ] Logs importantes archivados

## 🐛 Troubleshooting

Si algo falla, verifica:

### Error: "No handler.py file was found"
- [ ] `handler.py` está en la raíz del repo (no en subcarpeta)
- [ ] Archivo commiteado y pusheado correctamente
- [ ] Nombre del archivo es exactamente `handler.py` (case-sensitive)

### Error: "Module not found"
- [ ] Todas las dependencias en `requirements.txt`
- [ ] Versiones de paquetes compatibles
- [ ] No hay typos en nombres de paquetes

### Error: "CUDA out of memory"
- [ ] Instancia GPU tiene suficiente memoria
- [ ] Considerar aumentar tamaño de instancia
- [ ] Verificar que no hay memory leaks

### Error: "Model files not found"
- [ ] Todos los archivos .pt y .safetensors en el repo
- [ ] Archivos no están en .gitignore
- [ ] Git LFS configurado correctamente para archivos grandes

### Endpoint muy lento
- [ ] Aumentar tamaño de instancia
- [ ] Habilitar auto-scaling
- [ ] Optimizar código del handler
- [ ] Usar región más cercana

## 📞 Soporte

Si necesitas ayuda:

1. **Logs del Endpoint**: Revisa los logs en la UI de Hugging Face
2. **Documentación**: Consulta [DEPLOYMENT.md](./DEPLOYMENT.md)
3. **Ejemplos**: Revisa [ENDPOINT_USAGE.md](./ENDPOINT_USAGE.md)
4. **Comunidad**: Foro de Hugging Face
5. **Soporte**: support@huggingface.co

## 🎉 ¡Deployment Exitoso!

Si todos los checkboxes están marcados, ¡felicidades! Tu modelo está deployado y listo para producción.

---

**Última actualización**: Marzo 2026
**Versión del handler**: 1.0
**Modelo**: Chatterbox Multilingual TTS (23 idiomas)
