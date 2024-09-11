FROM python:3.8-slim

WORKDIR /app

ENV DOCKER_CONTAINER=1
ENV PYTHONUNBUFFERED=1

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

CMD ["python3", "run.py"]
