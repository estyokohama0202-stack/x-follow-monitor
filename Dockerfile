FROM python:3.11-slim

WORKDIR /app

COPY . .

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
    libxshmfence1 \
    libdrm2 \
    libxfixes3 \
    libxext6 \
    libx11-6 \
    libxcb1 \
    libxrender1 \
    libfontconfig1 \
    libpango-1.0-0 \
    libcairo2 \
    libatspi2.0-0 \
    libdbus-1-3 \
    libexpat1 \
    libuuid1 \
    libxcb-shm0 \
    libxcursor1 \
    libxi6 \
    libxtst6 \
    libnss3 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir -r requirements.txt
RUN python -m playwright install chromium

CMD ["python", "main.py"]
