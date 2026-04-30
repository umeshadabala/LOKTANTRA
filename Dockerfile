# ═══════════════════════════════════════════════════════════════
# LOKTANTRA: The Sovereign Saga — Optimized Multi-Stage Dockerfile
# Target: <500MB image, sub-second cold starts on Cloud Run
# ═══════════════════════════════════════════════════════════════

# ── Stage 1: Builder ────────────────────────────────────────────
FROM python:3.12-slim AS builder

# Install build dependencies for compiled packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Create virtual environment
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# ── Stage 2: Runtime ───────────────────────────────────────────
FROM python:3.12-slim AS runtime

# Install only runtime system libraries
RUN apt-get update && apt-get install -y --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

# Copy virtual environment from builder
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Set working directory
WORKDIR /app

# Copy application code
COPY main.py .
COPY app/ ./app/

# Create non-root user for security
RUN groupadd -r appuser && useradd -r -g appuser -d /app -s /sbin/nologin appuser
USER appuser

# Cloud Run uses PORT environment variable
ENV PORT=8080
ENV FLASK_ENV=production
ENV PYTHONUNBUFFERED=1

# Health check
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:${PORT}/health')" || exit 1

# Start with gunicorn for production
CMD exec gunicorn --bind :${PORT} --workers 2 --threads 4 \
    --timeout 120 --graceful-timeout 30 \
    --access-logfile - --error-logfile - \
    main:app
