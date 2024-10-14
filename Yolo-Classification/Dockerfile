# Your base image (replace with the appropriate one if different)
FROM nvidia/cuda:12.2.2-cudnn8-runtime-ubuntu20.04

# Add the deadsnakes PPA for Python 3.11
RUN apt-get update && apt-get install -y software-properties-common \
    && add-apt-repository ppa:deadsnakes/ppa \
    && apt-get update

# Install Python 3.11 and required packages
RUN apt-get install -y python3.11 python3.11-venv python3.11-dev curl libgl1

# Install pip for Python 3.11
RUN curl -sS https://bootstrap.pypa.io/get-pip.py -o get-pip.py \
    && python3.11 get-pip.py

# Verify that pip is installed using Python 3.11
RUN python3.11 -m pip --version

# # Create a symbolic link to pip3 for Python 3.11 if necessary
# RUN ln -s /usr/local/bin/pip /usr/local/bin/pip3 || true

# Set up alternatives for pip3
RUN update-alternatives --install /usr/bin/pip3 pip3 /usr/local/bin/pip3 1

# Set up alternatives for python3 to point to Python 3.11
RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.11 1


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

# # COPY Data to application code
# COPY ./datasets/Final /app/Final

# # Copy the image file into the container
# COPY datasets/Images/monitor2.png /app/datasets/Images/monitor2.png

# Set the working directory
WORKDIR /app
