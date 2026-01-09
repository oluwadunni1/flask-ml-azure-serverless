# Use Python 3.10 to match your Azure/Colab environment
FROM python:3.10-slim

# Set the working directory
WORKDIR /app

# Copy requirements first (better for Docker caching)
COPY requirements.txt .

# Install dependencies
# Added --no-cache-dir to keep image small
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose the port
EXPOSE 5000

# Define the command to start the application
CMD ["python", "app.py"]
