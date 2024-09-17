FROM python:3.8-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Install Playwright and its dependencies
RUN pip install playwright && playwright install-deps && playwright install

COPY . .

EXPOSE 5000

CMD ["python3.8", "run.py"]