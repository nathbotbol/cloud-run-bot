FROM python:3.11-slim

# Empêche les prompts pour gcloud
ENV CLOUDSDK_CORE_DISABLE_PROMPTS=1
ENV PATH=$PATH:/root/google-cloud-sdk/bin

# Installer les dépendances système pour gcloud
RUN apt-get update && apt-get install -y \
    curl \
    gnupg \
    lsb-release \
    sudo \
    unzip \
    && rm -rf /var/lib/apt/lists/*

# Installer Google Cloud SDK
RUN curl -fsSL https://sdk.cloud.google.com | bash

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY main.py .

# Port pour Cloud Run
ENV PORT 8080
EXPOSE 8080

CMD ["python", "main.py"]