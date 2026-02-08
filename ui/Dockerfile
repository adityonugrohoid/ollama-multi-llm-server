# UI service - optimized with only UI dependencies
FROM python:3.12-slim

WORKDIR /app

# Install only UI dependencies (no FastAPI)
COPY requirements-ui.txt .
RUN pip install --no-cache-dir -r requirements-ui.txt

# Copy UI code
COPY ui/ ./

# Run the Streamlit app
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
