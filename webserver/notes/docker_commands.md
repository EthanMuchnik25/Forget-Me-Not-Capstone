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


