# ==========================
# Dockerfile backend với PyTorch GPU
# ==========================
FROM pytorch/pytorch:2.1.0-cuda12.1-cudnn8-runtime

# Cài thêm ffmpeg, OpenCV
RUN apt-get update && apt-get install -y \
    ffmpeg \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy và cài requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY . .

EXPOSE 8000

CMD ["uvicorn", "main.server:app", "--host", "0.0.0.0", "--port", "8000"]
