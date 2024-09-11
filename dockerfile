FROM python:3.8-slim

ENV DOCKER_CONTAINER=1
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

CMD ["python3", "run.py"]
