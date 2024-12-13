# Step 1: Use the official Python image from DockerHub
FROM python:3.12-slim

# Step 2: Set the working directory
WORKDIR /webserver

# Step 3: Copy the current directory contents into the container
COPY . .

# Step 4: Install dependencies (including OpenCV dependencies)
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Step 5: Install the Python dependencies
RUN pip install -r requirements.txt

# Step 6: Install Nginx
RUN apt-get update && apt-get install -y nginx

# Step 7: Remove the default Nginx configuration file
RUN rm /etc/nginx/sites-enabled/default

# Step 8: Copy the custom Nginx config file into the container
COPY nginx.conf /etc/nginx/sites-available/nginx.conf
RUN ln -s /etc/nginx/sites-available/nginx.conf /etc/nginx/sites-enabled/

# Step 9: Expose port 80 to the outside world
EXPOSE 80

COPY /home/ethanm/.cache/huggingface/hub/models--dunzhang--stella_en_1.5B_v5 /root/.cache/huggingface/hub/models--dunzhang--stella_en_1.5B_v5

# Step 10: Start Nginx and Gunicorn
CMD service nginx start && gunicorn -c gunicorn.conf.py --workers 4 --bind 0.0.0.0:8000 myapp:app
