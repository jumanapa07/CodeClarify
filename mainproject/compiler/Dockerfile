# myapp/docker/Dockerfile

FROM python:3.12-slim

# Install dependencies using apt-get
RUN apt-get update && apt-get install -y \
    g++ \
    default-jdk

# Install Flask for running a simple HTTP server
RUN pip install Flask

# Copy the compilation script
COPY app.py /app/

# Set the working directory
WORKDIR /app

# Expose the Flask port
EXPOSE 5000

# Run the Flask app
CMD ["python", "/app/app.py"]
