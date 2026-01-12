# ----------------- Base image -----------------
FROM python:3.11-slim

# ----------------- System dependencies -----------------
RUN apt-get update && apt-get install -y \
    ffmpeg \
    libportaudio2 \
    netcat-openbsd \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# ----------------- Set working directory -----------------
WORKDIR /app

# ----------------- Copy requirements -----------------
COPY requirements.txt .

# ----------------- Upgrade pip and install Python packages -----------------
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# ----------------- Copy entire project -----------------
COPY . .

# ----------------- Make wait-for-db.sh executable -----------------
RUN chmod +x wait-for-db.sh

# ----------------- Expose port -----------------
EXPOSE 8080

# ----------------- Run FastAPI app with wait-for-db -----------------
CMD ["./wait-for-db.sh", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
