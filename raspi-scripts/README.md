# Raspi Scripts

__Fun fact__: If you plug your fan into the 5V and Ground pins, and point it at the heat sinks, the rpi will run substantially faster!


## Docs
For information on hardware specs, and hardware installation, go to [./notes/specs.md](./notes/specs.md)

For information regarding what each small script does, go to [./notes/small_scripts.md](./notes/small_scripts.md)

For information regarding the raspi_runtime scripts,  go to [./notes/raspi_runtime.md](./notes/raspi_runtime.md)

Here is the official documentation on how to set up a raspi for ssh: [https://www.raspberrypi.com/documentation/computers/remote-access.html](https://www.raspberrypi.com/documentation/computers/remote-access.html)\
Remember to reboot the machine after setting it up I think. 

## Directory Structure
```
/raspi-scripts
|
├── /small_scripts     # Assorted basic scripts, just so are stored in one location
├── /raspi-runtime     # Scripts that will be run on raspberry pi in final implementation
|
├── README.MD          # Primary documentation for directory
└── TEMP
```




