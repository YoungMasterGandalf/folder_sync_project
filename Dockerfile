FROM python:3.12-slim

WORKDIR /app

COPY . .

ENTRYPOINT ["python", "sync_folders.py"]