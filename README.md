This repository contains a python package to support programmatic interactions with the ITS preselector featuring an [x310 web relay](https://www.controlbyweb.com/x310/).
The package requires a SigMF metadata file that describes the Sensor preselector and a config file to describe the x310 settings for the rf paths specified in the 
metadata and for any other desired sources. Below is an example config file for the WebRelayPreselector to describe how it works:

```
{
  "base_url" : "http://192.168.130.32/state.xml?relay",
  "noise_diode_on" : "1State=1,2State=1,3State=0,4State=0",
  "noise_diode_off" : "1State=0,2State=1,3State=0,4State=0",
  "antenna" : "1State=0,2State=0,3State=0,4State=0",
  "1" : "1State=0,2State=1,3State=0,4State=0"
}
```

The base_url key is the only required key for the WebRelayPreselector and should map to the base url to interact with the WebRelay (see 
[https://www.controlbyweb.com/x310](https://www.controlbyweb.com/x310) for more info). The other keys should
correspond to RF paths documented in the SigMF metadata . In this example, 
there are noise_diode_on and noise_diode_off keys to correspond to the preselector paths to turn the noise diode on and off.
The name of the key in the config must match either the name or index of an RFPath defined in the preselector SigMF.
Each of the entries corresponding to RFPaths provide mappings to the associated web relay input states. 

# Installation and Usage
This repository is meant to be used as Python package. To install the package, clone the repository and enter the directory of the project in the command line (should be the same location as setup.cfg). Execute the following commands depending on your OS:
```
Windows:
py –m build 
py -m pip install dist/its-preselector-2.0.0.tar.gz 

Linux:
python3 -m build
Python3 –m pip install dist/its-preselector-2.0.0.tar.gz 

```
 

