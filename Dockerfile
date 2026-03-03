FROM python:3.11-slim

WORKDIR /app

# 必須ライブラリ（←ここが超重要）
RUN apt-get update && apt-get install -y \
    libglib2.0-0 \
    libnss3 \
    libatk-bridge2.0-0 \
    libgtk-3-0 \
    libgbm1 \
    libasound2 \
    libx11-xcb1 \
    libxcomposite1 \
    libxdamage1 \
    libxrandr2 \
    libxfixes3 \
    libxext6 \
    libxi6 \
    libxtst6 \
    libpango-1.0-0 \
    libcairo2 \
    fonts-liberation \
    wget \
    && rm -rf /var/lib/apt/lists/*

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

# Playwright
RUN python -m playwright install chromium

CMD ["python", "main.py"]
