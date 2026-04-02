FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PORT=8080

WORKDIR /app

# Create non-root runtime user
RUN addgroup --system app && adduser --system --ingroup app app

# Install dependencies first for better layer caching
COPY app/requirements.txt /tmp/requirements.txt
RUN pip install --upgrade pip && \
    pip install -r /tmp/requirements.txt

# Copy source
COPY . /app
RUN chown -R app:app /app

USER app

EXPOSE 8080

# Cloud Run-compatible startup
CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${PORT} --workers 1"]