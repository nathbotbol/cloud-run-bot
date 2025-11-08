FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY main.py .

# GCP SDK déjà disponible sur certaines images, sinon installer ici
# RUN apt-get update && apt-get install -y curl && curl https://sdk.cloud.google.com | bash

CMD ["python", "main.py"]