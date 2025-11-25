# ==== Base image với PyTorch + CUDA ====
FROM pytorch/pytorch:2.1.0-cuda12.1-cudnn8-runtime

# ==== System dependencies (cache-friendly, retry-able) ====
RUN apt-get update --fix-missing && \
    apt-get install -y --no-install-recommends \
        ffmpeg \
        libgl1 \
        libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# ==== Workdir ====
WORKDIR /app

# ==== Copy & install Python dependencies ====
COPY requirements.txt .
RUN pip install --upgrade pip setuptools wheel && \
    pip install --no-cache-dir -r requirements.txt

# ==== Copy TSM ops module ====
COPY tsm/temporal-shift-module/ops /app/ops

# ==== Copy remaining backend source code ====
COPY . .

# ==== Set PYTHONPATH ====
ENV PYTHONPATH=/app

# ==== Expose port ====
EXPOSE 8000

# ==== Run server ====
CMD ["uvicorn", "main.server:app", "--host", "0.0.0.0", "--port", "8000"]
