# Use official Python slim image
FROM python:3.11-slim

# Set working directory inside container
WORKDIR /app

# Copy requirements and install deps
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all code files
COPY scraper.py .
COPY cookies.txt .

# Run the scraper script by default
CMD ["python", "scraper.py"
