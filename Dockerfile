FROM python:3.11-slim
WORKDIR /app

# Install git if needed for any pip installs
RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml .
# Install dependencies first (for caching)
RUN pip install --no-cache-dir .

COPY . .
# Install the package itself in editable mode or normally
RUN pip install --no-cache-dir -e .

EXPOSE 8000
CMD ["uvicorn", "server.app:app", "--host", "0.0.0.0", "--port", "8000"]
