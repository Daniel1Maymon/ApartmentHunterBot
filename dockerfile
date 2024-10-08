FROM python:3.8-slim

ENV FLASK_ENV=development

WORKDIR /app

COPY req2.txt ./requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

RUN apt-get update && apt-get install -y \
    libglib2.0-0 libnss3 libnspr4 libdbus-1-3 libatk1.0-0 \
    libatk-bridge2.0-0 libcups2 libdrm2 libxcb1 libxkbcommon0 \
    libatspi2.0-0 libx11-6 libxcomposite1 libxdamage1 libxext6 \
    libxfixes3 libxrandr2 libgbm1 libpango-1.0-0 libcairo2 libasound2

# Install Playwright and its dependencies
# RUN pip install playwright && playwright install-deps && playwright install
RUN pip install playwright && playwright install chromium

COPY . .

EXPOSE 5000

CMD ["python3.8", "-u", "run.py"]
