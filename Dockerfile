# Use Python 3.11 slim image as base - smaller than full Python image
# Alpine could be even smaller but may have compatibility issues with some packages
FROM python:3.11-slim

# Set environment variables
# PYTHONDONTWRITEBYTECODE: Prevents Python from writing pyc files to disc
# PYTHONUNBUFFERED: Prevents Python from buffering stdout and stderr
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Set work directory inside container
# All subsequent commands will run from this directory
WORKDIR /app

# Install system dependencies
# We need these for MySQL connector and other packages
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        gcc \
        default-libmysqlclient-dev \
        pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better Docker layer caching
# If requirements.txt doesn't change, Docker can reuse this layer
COPY requirements.txt .

# Install Python dependencies
# --no-cache-dir saves space by not storing pip cache
# --upgrade ensures we get latest versions
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copy application code
# We do this after installing dependencies so code changes don't invalidate dependency layer
COPY . .

# Create a non-root user for security
# Running as root in containers is a security risk
RUN adduser --disabled-password --gecos '' appuser \
    && chown -R appuser:appuser /app
USER appuser

# Expose port 8000
# This is the port FastAPI will run on inside the container
EXPOSE 8000

# Health check to ensure container is running properly
# This helps Kubernetes know if the container is healthy
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/ || exit 1

# Command to run the application
# --host 0.0.0.0 makes it accessible from outside the container
# --port 8000 specifies the port
# --workers 1 for development, increase for production
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "1"]