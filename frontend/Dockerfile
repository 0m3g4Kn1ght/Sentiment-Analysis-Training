# frontend/Dockerfile
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt ./frontend/requirements.txt
RUN pip install --no-cache-dir -r frontend/requirements.txt

COPY . ./frontend

EXPOSE 8501

# Streamlit needs to run from the folder where app.py is
WORKDIR /app/frontend
CMD ["streamlit", "run", "app.py", "--server.port", "8501", "--server.address", "0.0.0.0"]
