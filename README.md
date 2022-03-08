This repository contains a python package to support programmatic interactions with an RF preselector. 
The package defines an abtract Preselector class that defines a simple interface for any preselector. 
Currently, the WebRelayPreselector class in web_relay_preselector is the only implementation of the Preselector.
The WebRelayPreselector supports a preselector featuring an [x310 WebRelay](https://www.controlbyweb.com/x310/).
The package requires a [SigMF metadata file](https://Github.com/NTIA/sigmf-ns-ntia) that describes the Sensor preselector and a config file to describe the x310 settings for the rf paths specified in the 
metadata and for any other desired sources. Below is an example config file for the WebRelayPreselector to describe how it works:
```
{
  "base_url" : "http://192.168.130.32/state.xml?relay",
  "noise_diode_on" : "1State=1,2State=1,3State=0,4State=0",
  "noise_diode_off" : "1State=0,2State=1,3State=0,4State=0",
  "antenna" : "1State=0,2State=0,3State=0,4State=0"
}
```

The base_url key is the only required key for the WebRelayPreselector and should map to the base url to interact with the WebRelay (see 
[https://www.controlbyweb.com/x310](https://www.controlbyweb.com/x310) for more info). The other keys should
correspond to RF paths documented in the SigMF metadata. Each of the entries in the 
config provide mappings to the associated web relay input states and every RFPath defined 
in the sensor definition json file should have an entry in the preselector config. The keys in the dictionary may use
the name of the RFPath or the index of the RFPath in the RFPaths array. 
In this example, there are noise_diode_on and noise_diode_off keys to correspond to the preselector paths to turn the noise diode on and off, an antenna key to indicate the web relay states to connect to the antenna. 
Note: with this example configuration, you would have to set the path by the name of the source rather than the index in 
the rf_paths array within the preselector definition in the SigMf metadata file. 
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
#Contact 
For technical questions, contact Doug Boulware, dboulware@ntia.gov

