# Using an official Python runtime as a parent image
FROM python:3.9-slim

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

# Exposing port 5000 for Flask
EXPOSE 5000

# Run app.py when the container launches
CMD ["python", "app.py"]
