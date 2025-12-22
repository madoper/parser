# SEMANTIC: Multi-stage build for optimized Python backend container

# Stage 1: Builder stage for dependencies
FROM python:3.11-slim as builder

# SEMANTIC: Set working directory for build
WORKDIR /app

# SEMANTIC: Install system dependencies for Python packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    g++ \
    libxml2-dev \
    libxslt1-dev \
    zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*

# SEMANTIC: Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# Stage 2: Runtime stage with minimal footprint
FROM python:3.11-slim

# SEMANTIC: Set environment variables for Python
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PATH=/home/parser/.local/bin:$PATH

# SEMANTIC: Create non-root user for security
RUN useradd -m -u 1000 parser && \
    mkdir -p /app && \
    chown -R parser:parser /app

# SEMANTIC: Set working directory
WORKDIR /app

# SEMANTIC: Install runtime dependencies only
RUN apt-get update && apt-get install -y --no-install-recommends \
    libxml2 \
    libxslt1.1 \
    && rm -rf /var/lib/apt/lists/*

# SEMANTIC: Copy installed dependencies from builder
COPY --chown=parser:parser --from=builder /root/.local /home/parser/.local

# SEMANTIC: Copy application code
COPY --chown=parser:parser . .

# SEMANTIC: Switch to non-root user
USER parser

# SEMANTIC: Expose application port
EXPOSE 8000

# SEMANTIC: Health check endpoint
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')"

# SEMANTIC: Run application with uvicorn
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
