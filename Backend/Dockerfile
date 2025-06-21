# Use Python base image
FROM python:3.10-slim

# Create work directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy app code
COPY . .

# Expose Flask port
EXPOSE 5000

# Run the app using Python directly
CMD ["python3", "app.py"]
