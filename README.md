# NTIA/ITS Preselector API

![GitHub release (latest SemVer)](https://img.shields.io/github/v/release/NTIA/Preselector?display_name=tag&sort=semver)
![GitHub all releases](https://img.shields.io/github/downloads/NTIA/Preselector/total)
![GitHub issues](https://img.shields.io/github/issues/NTIA/Preselector)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

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

## Table of Contents

- [Introduction](#introduction)
- [Usage](#usage)
- [Development](#development)
- [License](#license)
- [Contact](#contact)

## Introduction

A preselector is a device, connected between an antenna and a signal analyzer, designed to
improve the RF performance and capability of a sensor. As illustrated in the diagram below,
it may include a variety of components, e.g., filters, amplifiers, calibration sources, and
switches. An example preselector is shown in Figure 1. Just as the components within a preselector
may change, so too may the way in which the switching is controlled.

![Preselector Diagram](/docs/img/preselector.png)
<figcaption>Figure 1: Block diagram showing an example RF measurement system with a preselector.</figcaption>

## Usage

To install this Python package, clone the repository and enter the directory of the
project in the command line. Execute the following commands depending on your OS (you may
have to adjust for your version of Python):

```bash
# Windows
py -m pip install .

# Linux
python3 –m pip install .
```

### `WebRelayPreselector` Configuration

The `WebRelayPreselector` requires a [SigMF metadata file](https://Github.com/NTIA/sigmf-ns-ntia)
that describes the sensor preselector and a config file to describe the x310 settings for
the RF paths specified in the metadata and for any other desired sources. Below is an
example config file for the `WebRelayPreselector` to describe how it works:

```json
{
  "name": "preselector",
  "base_url" : "http://192.168.1.2/state.xml",
  "control_states": {
      "noise_diode_on" : "1State=1,2State=1,3State=0,4State=0",
      "noise_diode_off" : "1State=1,2State=0,3State=0,4State=0",
      "antenna" : "1State=0,2State=0,3State=0,4State=0"
  },
  "status_states": {
    "noise diode powered" : "relay2=1",
    "antenna path enabled": "relay1=0",
    "noise diode path enabled": "relay1=1"
  },
  "sensors": {
    "internal_temp": 1,
    "internal_humidity": 2,
    "tec_intake_temp": 3,
    "tec_exhaust_temp": 4
  },
  "digital_inputs": {
      "ups_power": 1,
      "ups_battery_level": 2,
      "ups_trouble": 3,
      "ups_battery_replace": 4
  },
  "analog_inputs": {
      "door_sensor": 1,
      "5vdc_monitor": 2,
      "28vdc_monitor": 3,
      "15vdc_monitor": 4,
      "24vdc_monitor": 5
  }
}
```

The `base_url` and `name` keys are the only required keys for the `WebRelayPreselector`.
The `base_url` should map to the base URL to interact with the WebRelay
(see [https://www.controlbyweb.com/x310](https://www.controlbyweb.com/x310)
for more info). The keys within the control_states key should correspond to RF paths
documented in the SigMF metadata. The keys within the status_states should map to the
RF paths documented in the SigMF metadata, or to understandable states of the
preselector for which it is desired to determine whether they are enabled or disabled.
The status method of the preselector will provide each of the keys specified in the
status_states entry mapped to a boolean indicating whether the preselector states match
those specified in the mapping. Each of the entries in the config provide mappings to the
associated web relay input states and every RFPath defined in the sensor definition json
file should have an entry in the preselector config. The keys in the dictionary may use the
name of the RFPath or the index of the RFPath in the RFPaths array.
The `sensors`, `digital_inputs`, and `analog_inputs` keys define the sensors,
digital_inputs and analog_inputs configured on the device. Within each of the sections,
each key provides the name of the sensor or input and the value specifies the assigned
sensor or input number. The get_satus method will provide each sensor/input value with
the specified label.

In this example, there are `noise_diode_on` and `noise_diode_off` keys to correspond to the
preselector paths to turn the noise diode on and off, and an antenna key to indicate the
web relay states to connect to the antenna.

Note: with this example configuration, you would have to set the path by the name of the
source rather than the index in the `rf_paths` array.

### `WebRelayPreselector` Initialization

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

### Preselector Interactions

#### Access instance properties

- `preselector.amplifiers[0].gain`
- ...

#### Helper methods

- `preselector.get_amplifier_gain(rf_path_index)`
- `preselector.get_amplifier_noise_figure(rf_path_index)`
- `preselector.get_frequency_low_passband(rf_path_index)`
- `preselector.get_frequency_high_passband(rf_path_index)`
- `preselector.get_frequency_low_stopband(rf_path_index)`
- `preselector.get_frequency_high_stopband(rf_path_index)`

#### Control

- `preselector.set_state(rf_path_name)`

## Development

Set up a development environment using a tool like [Conda](https://docs.conda.io/en/latest/)
or [venv](https://docs.python.org/3/library/venv.html#module-venv), with `python>=3.7`. Then,
from the cloned directory, install the development dependencies by running:

```bash
pip install .[dev]
```

This will install the project itself, along with development dependencies for pre-commit
hooks, building distributions, and running tests. Set up pre-commit, which runs
auto-formatting and code-checking automatically when you make a commit, by running:

```bash
pre-commit install
```

The pre-commit tool will auto-format Python code using [Black](https://github.com/psf/black)
and [isort](https://github.com/pycqa/isort). Other pre-commit hooks are also enabled, and
can be found in [`.pre-commit-config.yaml`](.pre-commit-config.yaml).

### Building New Releases

This project uses [Hatchling](https://github.com/pypa/hatch/tree/master/backend) as a backend.
Hatchling makes versioning and building new releases easy. The package version can be updated
easily by using any of the following commands.

```bash
hatchling version major   # 1.0.0 -> 2.0.0
hatchling version minor   # 1.0.0 -> 1.1.0
hatchling version micro   # 1.0.0 -> 1.0.1
hatchling version "X.X.X" # 1.0.0 -> X.X.X
```

To build a new release (both wheel and sdist/tarball), run:

```bash
hatchling build
```

## License

See [LICENSE](LICENSE.md)

## Contact

For technical questions, contact Doug Boulware, dboulware@ntia.gov
