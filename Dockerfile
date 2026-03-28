# Dockerfile para RunPod - Chatterbox TTS Español
FROM runpod/pytorch:2.1.0-py3.10-cuda11.8.0-devel-ubuntu22.04

# Configurar directorio de trabajo
WORKDIR /app

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    git \
    git-lfs \
    libsndfile1 \
    ffmpeg \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements primero (para cache de Docker)
COPY requirements.txt .

# Instalar dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir runpod

# Copiar código fuente
COPY src/ /app/src/
COPY runpod_handler.py /app/

# Configurar variables de entorno
ENV PYTHONUNBUFFERED=1
ENV CUDA_VISIBLE_DEVICES=0

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD python -c "import torch; print(torch.cuda.is_available())" || exit 1

# Comando de inicio
CMD ["python", "-u", "runpod_handler.py"]
