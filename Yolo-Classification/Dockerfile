# Your base image (replace with the appropriate one if different)
FROM nvidia/cuda:12.2.2-cudnn8-runtime-ubuntu20.04

# Install Python and dependencies
# Update package list and install prerequisites
RUN apt-get update && apt-get install -y \
    software-properties-common \
    && add-apt-repository ppa:deadsnakes/ppa \
    && apt-get update

# Install Python 3.11 and pip for Python 3.11
RUN apt-get install -y python3.11 python3.11-venv python3.11-dev python3-pip

# # Install system dependencies
# RUN apt-get update && apt-get install -y \
#     libgl1-mesa-glx \
#     libglib2.0-0 \
#     && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . /app

# Copy the image file into the container
COPY datasets/Images/monitor2.png /app/datasets/Images/monitor2.png

# Set the working directory
WORKDIR /app

# Run your application
CMD ["python", "FiftyOne.py", "-t"]
