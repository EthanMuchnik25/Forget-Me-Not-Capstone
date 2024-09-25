# nginx Notes

### If you would like to learn how to modify nginx.conf, a few notes can be found farther down this document.

## How to disable nginx run on system reboot:
By default, nginx is set to run when your system reboots. To check if this is currently the case, type:
```
sudo systemctl is-enabled nginx
```

To turn this behavior off, type:
```
sudo systemctl disable nginx
```


## Debugging Tips:

### How to know if nginx is running:
```
sudo systemctl status nginx # or
sudo service nginx status
```
#### Debugging tips:
idk, this always worked for me, probably ask chatgpt

### To check if the port is listening correctly, type:
```
sudo netstat -tuln | grep 80 # or
curl -I http://localhost
```
#### Deugging tips:

After running the curl command, I have gotten the following errors:
1. `curl: (7) Failed to connect to localhost port 80 after 0 ms: Couldn't connect to server` - nginx not working, maybe check config file structure?
2. `HTTP/1.1 502 Bad Gateway...` - flask is probably not running

#### If port 80 is not working, and you have tried the obvious checks, try these steps:
Check your firewall. If you have iptables, run:
```
sudo iptables -L -n -v
```
The `INPUT` section should not block 80, `policy ACCEPT` means all connections are otherwise accepted.

Check the nginx error logs:
```
sudo tail -f /var/log/nginx/error.log
```
You can adjust the number of lines shown with -n \<num\> if the default 10 is not enough. 


## Notes on modifying nginx.conf:

Modifying nginx.conf should probably be done if you'd like to modify what html files are served for which user inputs. If you run into issues, you may have better luck just asking ChatGPT, but here are some issues I ran into:

### Location Field:
Locations can be weird. In order for all default requests to go to flask, I wanted a separate location to serve a default html file. I tried having my location field look like this:
```
location /test {
        root /var/www/html;
        index index.nginx-debian.html;
    }
}
```
On my laptop, `index.nginx-debian.html` is located at `var/www/html/`. However, this location causes nginx to look for the file at `var/www/html/test/`. Importantly, the `root` field defines the root directory for requests that match the location block, and the `index` field specifies the default file to serve when a directory is requested.

As this is a bit of an edge case, and used for testing, we can hard-code the block to return the file like this:

```
location /test {
        alias /var/www/html/index.nginx-debian.html; 
}
```
However, this should probably be changed in the future.

### Verbose Logging
If you'd like verbose logging enabled for debugging, add or uncomment the followign line to the `server` block:
```
error_log /var/log/nginx/error.log debug;
```