FROM python:3.9-slim

WORKDIR /app

# Copy requirements first to leverage Docker cache
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy the rest of the application
COPY . .

# Make sure models directory exists
RUN mkdir -p models

EXPOSE 5001

# Command to run the application
CMD ["python", "app.py"]
