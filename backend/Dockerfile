FROM pytorch/pytorch:2.1.0-cuda12.1-cudnn8-runtime

# Install system dependencies
RUN apt-get update && apt-get install -y \
    ffmpeg \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Force NumPy <2 to avoid compatibility issues
RUN pip install --no-cache-dir "numpy<2"

# Copy requirements
COPY requirements.txt .

# Install Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy temporal-shift-module → ops
COPY tsm/temporal-shift-module/ops /app/ops

# Copy remaining backend source code
COPY . .

# Set PYTHONPATH to /app
ENV PYTHONPATH=/app

EXPOSE 8000

# Run server
CMD ["uvicorn", "main.server:app", "--host", "0.0.0.0", "--port", "8000"]
