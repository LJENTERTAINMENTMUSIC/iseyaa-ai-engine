# ISEYAA API - FastAPI Dockerfile
FROM python:3.14-slim AS base

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
# Root requirements.txt or app specific? 
# Usually, in a monorepo, you might have one at the root or per-app.
# Currently, it was looking in apps/api/requirements.txt
COPY apps/ai-engine/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
# We copy the entire apps/ai-engine to /app/apps/ai-engine
COPY apps/ai-engine/ /app/apps/ai-engine/
COPY packages/ai_agents/ /app/packages/ai_agents/

# Set working directory to the app directory for easier execution and imports
WORKDIR /app/apps/ai-engine

# Create non-root user
RUN useradd --create-home --uid 1000 appuser
RUN chown -R appuser:appuser /app
USER appuser

EXPOSE 8000

# Set PYTHONPATH to include the app directory and packages
ENV PYTHONPATH=/app:/app/apps/ai-engine:/app/packages/ai_agents

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
