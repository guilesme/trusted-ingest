FROM python:3.12-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app
COPY requirements.txt .

EXPOSE 8080
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]

FROM base AS cpu
COPY constraints-cpu.txt .
# Obtain the CPU wheels explicitly, then constrain the application resolver.
RUN pip install --no-cache-dir --index-url https://download.pytorch.org/whl/cpu -r constraints-cpu.txt \
    && pip install --no-cache-dir -r requirements.txt -c constraints-cpu.txt \
    && pip check
COPY app ./app

# Keep the original dependency source and default build behavior for rollback.
FROM base AS default
RUN pip install --no-cache-dir -r requirements.txt
COPY app ./app
