# NTIA/ITS Preselector API

This repository provides a general software API to control preselectors regardless of their
components and control mechanisms.

Currently, this API provides a general abstract `Preselector` class that uses an `rf_path`
array to describe the available combinations of calibration sources, filters, and amplifiers.
A simple `set_state` method allows users to specify the state of the preselector by the state
key specified in the preselector config. Different switching control mechanisms are supported
by extending the base `Preselector` class. Currently, this repository provides an implementation
for a `WebRelayPreselector` that includes an [x310 WebRelay](https://www.controlbyweb.com/x310/).
See below for additional details on using the `WebRelayPreselector`.  

This software will grow over time to support additional components and control mechanisms.

## Introduction

 A preselector is a device, connected between an antenna and a signal analyzer, designed to
 improve the RF performance and capability of a sensor. As illustrated in the diagram below,
 it may include a variety of components, e.g., filters, amplifiers, calibration sources, and
 switches. An example preselector is shown in Figure 1. Just as the components within a preselector
 may change, so too may the way in which the switching is controlled.

![Preselector Diagram](/docs/img/preselector.png)
<p style="text-align: center;"><figcaption align = "center"><b>Figure.1 - Example Preselector</b></figcaption></p>


## Installation

To install this Python package, clone the repository and enter the directory of the project in
the command line (should be the same location as `setup.cfg`). Execute the following commands
depending on your OS (you may have to adjust for your version of Python):

```bash
# Windows
py –m build 
py -m pip install dist/its-preselector-2.0.1.tar.gz 

# Linux
python3 -m build
python3 –m pip install dist/its-preselector-2.0.1.tar.gz 

```

## `WebRelayPreselector` Configuration

The `WebRelayPreselector` requires a [SigMF metadata file](https://Github.com/NTIA/sigmf-ns-ntia)
that describes the sensor preselector and a config file to describe the x310 settings for the RF
paths specified in the metadata and for any other desired sources. Below is an example config file
for the `WebRelayPreselector` to describe how it works:

```json
{
  "base_url" : "http://192.168.130.32/state.xml",
  "noise_diode_on" : "1State=1,2State=1,3State=0,4State=0",
  "noise_diode_off" : "1State=0,2State=1,3State=0,4State=0",
  "antenna" : "1State=0,2State=0,3State=0,4State=0"
}
```

The `base_url` key is the only required key for the `WebRelayPreselector` and should map to the
base URL to interact with the WebRelay (see [https://www.controlbyweb.com/x310](https://www.controlbyweb.com/x310)
for more info). The other keys should correspond to RF paths documented in the SigMF metadata.
Each of the entries in the config provide mappings to the associated web relay input states and
every RFPath defined in the sensor definition json file should have an entry in the preselector
config. The keys in the dictionary may use the name of the RFPath or the index of the RFPath in
the RFPaths array.

In this example, there are `noise_diode_on` and `noise_diode_off` keys to correspond to the
preselector paths to turn the noise diode on and off, and an antenna key to indicate the web
relay states to connect to the antenna.

Note: with this example configuration, you would have to set the path by the name of the source
rather than the index in the `rf_paths` array.

## `WebRelayPreselector` Initialization

```python
import json
from its_preselector.web_relay_preselector import WebRelayPreselector


with open('config/metadata.sigmf-meta') as sensor_def_file:
    sensor_def = json.load(sensor_def_file)

with open('config/config.json') as config_file:
    preselector_config = json.load(config_file)

preselector = WebRelayPreselector(sensor_def, preselector_config)
preselector.set_state('antenna')
```

## Preselector Interactions

### Access instance properties

- `preselector.amplifiers[0].gain`
- ...

### Helper methods

- `preselector.get_amplifier_gain(rf_path_index)`
- `preselector.get_amplifier_noise_figure(rf_path_index)`
- `preselector.get_frequency_low_passband(rf_path_index)`
- `preselector.get_frequency_high_passband(rf_path_index)`
- `preselector.get_frequency_low_stopband(rf_path_index)`
- `preselector.get_frequency_high_stopband(rf_path_index)`

### Control

- `preselector.set_state(rf_path_name)`

## License

See [LICENSE](LICENSE.md).

## Contact

For technical questions, contact Doug Boulware, dboulware@ntia.gov
