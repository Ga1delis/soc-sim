FROM python:3.11-slim
RUN apt-get update && apt-get install -y \
    git build-essential cmake libopenblas-dev wget curl \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /app
COPY . /app
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
CMD ["python", "/app/simulation/run.py"]