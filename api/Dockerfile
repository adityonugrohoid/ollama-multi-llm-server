# API service - optimized with only API dependencies
FROM python:3.12-slim

WORKDIR /app

# Install only API dependencies (no Streamlit)
COPY requirements-api.txt .
RUN pip install --no-cache-dir -r requirements-api.txt

# Copy API code
COPY api/ ./

# Run the FastAPI service
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
