This repository contains a python package to support programmatic interactions with the ITS preselector featuring an [x310 web relay](https://www.controlbyweb.com/x310/).
The package requires a SigMF metadata file that describes the Sensor preselector and a config file to describe the x310 settings for the rf paths specified in the 
metadata and for any other desired sources. Below is an example config file to describe how it works:

```
[WEB_RELAY]
base_url=http://192.168.130.32/state.xml?relay

[NOISE_DIODE]
on=1State=1,2State=1,3State=0,4State=0
off=1State=0,2State=1,3State=0,4State=0

[0]
on=1State=0,2State=1,3State=0,4State=0
off=1State=0,2State=0,3State=0,4State=0
```

The first WEB_RELAY section is required for any config file and must have the base_url to connect to the web relay. The subsequent sections
correspond to RF paths documented in the SigMF metadata or any other sources that may or may not be documented in the metadata. In this example, 
there is a NOISE_DIODE section to support turning the noise diode on and off. Below each source section there must be on and off mappings. 
These entries provide mappings to the associated web relay input states. Config sections labeled with a number represent the on/off configurations for the RF Paths documented
in the SigMF metadata. So, in the above example the [0] section defines the on/off settings for the first RF Path, or 0 indexed RF Path. 

# Installation and Usage
This repository is meant to be used as Python package. To install the package, clone the repository and enter the directory of the project in the command line (should be the same location as setup.cfg). Execute the following commands depending on your OS:
```
Windows:
py –m build 
py -m pip install dist/its-preselector-0.0.1.tar.gz 

Linux:
python3 -m build
Python3 –m pip install dist/its-preselector-0.0.1.tar.gz 

```
 

