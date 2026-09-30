FROM python:3.13-slim

# Prevent Python from creating .pyc files
# and make logs appear immediately
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Application directory
WORKDIR /app

# Install Python dependencies first
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copy application source
COPY . .

# Streamlit port
EXPOSE 8501

# Start ResearchMind
CMD ["streamlit", "run", "app.py", "--server.address=0.0.0.0", "--server.port=8501"]