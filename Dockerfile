FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

RUN apk add --no-cache \
    ffmpeg \
    libavc1394 \
    tini

COPY . .

EXPOSE 3005

CMD ["python", "worker.worker"]