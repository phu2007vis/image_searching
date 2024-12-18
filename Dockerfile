FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app/main
COPY requirements_server.txt requirements_server.txt

# Install wget
RUN apt-get update && apt-get install -y wget

# Download the required file using wget
# RUN wget -O /app/main/vgg_transformer.pth https://vocr.vn/data/vietocr/vgg_transformer.pth

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements_server.txt


# Change working directory to /app/main
WORKDIR /app/main