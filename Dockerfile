FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy files to container
COPY app.py ./

# Install dependencies
RUN pip install flask

# Expose port
EXPOSE 5000

# Run the server
CMD ["python", "./app.py"]

