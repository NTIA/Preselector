# Introduction
As shown in the example diagram below, a preselector is a device connected between an antenna and a signal analyzer designed to improve the performance of an RF sensor. 
A preselector may include a variety of components including, but not limited to, filters, amplifiers, 
calibration sources, and switches to control the components through which the RF signal flows.
![Preselector Diagram](/docs/img/preselector.png)
Just as the components within a preselector may change, so too may the way in which the switching is controlled.
This repository provides a general software API to interface with preselectors regardless of their components and control mechanisms. Because of the general nature of this software and the variety of components and control mechanisms that may be used within a preselector it should be expected that this software will grow over time to support additional components and control mechanisms.
Currently, this API provides a general abstract Preselector class that may consist of any number of filters, amplifiers, and calibration sources. 
In addition, the preselector class uses a collection of rf_paths to describe the combinations of calibration sources, filters, a
nd amplifiers that may be connected based on the internal switches. A simple set_rf_path method allows users to control which rf path is configured in the preselector. 
Finally, different switching control mechanisms are supported by extending the base Preseelctor class. Currently, this repository provides a implementation for a WebRelayPreselector that includes an [x310 WebRelay](https://www.controlbyweb.com/x310/). See below for additional details on using the WebRelayPreslector.  

# Installation 
To install this Python package, clone the repository and enter the directory of the project in the command line (should be the same location as setup.cfg). Execute the following commands depending on your OS (you may have to adjust for your version of python):
```
Windows:
py –m build 
py -m pip install dist/its-preselector-2.0.0.tar.gz 

Linux:
python3 -m build
Python3 –m pip install dist/its-preselector-2.0.0.tar.gz 

```
#WebRelayPreselector Configuration
The WebRelayPreselector requires a [SigMF metadata file](https://Github.com/NTIA/sigmf-ns-ntia) that describes the Sensor preselector and a config file to describe the x310 settings for the rf paths specified in the 
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
In this example, there are noise_diode_on and noise_diode_off keys to correspond to the preselector paths to turn the noise diode on and off, and an antenna key to indicate the web relay states to connect to the antenna. 
Note: with this example configuration, you would have to set the path by the name of the source rather than the index in 
the rf_paths array.

# WebRelayPreselector Initialization
```
import json
from its_preselector.web_relay_preselector import WebRelayPreselector
import json


with open('config/metadata.sigmf-meta') as sensor_def_file:
    sensor_def = json.load(sensor_def_file)

with open('config/config.json') as config_file:
    preselector_config = json.load(config_file)

preselector = WebRelayPreselector(sensor_def, preselector_config)
```

# Preselector Interactions

## Access instance properties
<ul>
<li>preselector.amplifiers[0].gain</li>
<ii>...</ii>
</ul>

## Helper methods:
<ul>
<li>preselector.get_amplifier_gain(rf_path_index)</li>
<li>preselector.get_amplifier_noise_figure(rf_path_index)</li>
<li>preselector.get_frequency_low_passband(rf_path_index)</li>
<li>preselector.get_frequency_high_passband(rf_path_index)</li>
<li>preselector.get_frequency_low_stopband(rf_path_index)</li>
<li>preselector.get_frequency_high_stopband(rf_path_index)</li>
</ul>

## Control:
 <ul>
<li>preselector.set_rf_path(rf_path_name)</li>
</ul>

#Contact 
For technical questions, contact Doug Boulware, dboulware@ntia.gov

