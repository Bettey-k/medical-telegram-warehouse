FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    git \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Dagster requirement (already correct)
RUN mkdir -p /tmp/dagster
ENV DAGSTER_HOME=/tmp/dagster

EXPOSE 3000

CMD ["dagster", "dev", "-f", "pipeline.py", "--host", "0.0.0.0"]
