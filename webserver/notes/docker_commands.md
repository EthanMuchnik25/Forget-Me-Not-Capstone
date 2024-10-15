# Some Random Docker Commands

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


