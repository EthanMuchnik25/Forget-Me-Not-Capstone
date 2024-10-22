# Some Random Docker Commands

## Build and run

### Build image:
```
docker build -t myapp .
```

### Run docker container:
```
docker run -p 4000:80 myapp
```

### Enter docker container with shell
```
docker exec -it myapp /bin/bash
```

### Flag to attach volume to container
```
-v $(pwd)/my-local-dir:/webserver
```

## Container management

### List all docker containers
```
docker ps -a
```

### List docker images
```
docker images
```

### Stop docker container
```
docker stop <container-id>
```

### Remove docker container
```
docker stop <container_id_or_name>
```

### Remove docker image
```
docker rmi <image_id>
```

## Install docker (debian)

Website: [https://docs.docker.com/engine/install/debian/](https://docs.docker.com/engine/install/debian/)\
I think this works for all debian-based 64 bit linux OS, which raspberry pi is.\

Uninstall old version
```
for pkg in docker.io docker-doc docker-compose podman-docker containerd runc; do sudo apt-get remove $pkg; done
```

Set up docker apt repo
```
# Add Docker's official GPG key:
sudo apt-get update
sudo apt-get install ca-certificates curl
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/debian/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc

# Add the repository to Apt sources:
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/debian \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get update
```

Install docker packages (latest)
```
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```

Verify
```
sudo docker run hello-world
```

## Want to don't need sudo for docker commands (linux)
```
sudo groupadd docker
```
```
sudo usermod -aG docker $USER
```
Log out and log back in

Verify change
```
docker ps
```