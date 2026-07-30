# Stage 1: Base image
FROM python:3.11-slim

# Create a system user and group for security
RUN groupadd -r appuser && useradd -r -g appuser appuser

# Set working directory
WORKDIR /app

# Install system dependencies if needed
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application source code
COPY . /app

# Change ownership of the app directory to the non-root user
RUN chown -R appuser:appuser /app

# Switch to non-root user
USER appuser

# Expose API port
EXPOSE 5000

# Run the application
CMD ["python", "app.py"]
