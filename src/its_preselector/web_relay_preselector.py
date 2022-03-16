from its_preselector.preselector import Preselector
import requests
import xml.etree.ElementTree as ET


class WebRelayPreselector(Preselector):

    def __init__(self, sigmf, config):
        super().__init__(sigmf, config)
        if 'base_url' in config:
            self.base_url = config['base_url']

    def set_rf_path(self, i):
        key = str(i)
        if key in self.config:
            switches = self.config[str(i)].split(',')
            if self.base_url:
                for i in range(len(switches)):
                    command = self.base_url + '?relay'+ switches[i]
                    print(command)
                    requests.get(command)
        else:
            raise Exception("RF path " + key + " configuration does not exist.")


    def get_sensor_value(self, sensor_num):
        sensor_num_string =  str(sensor_num)
        response = requests.get(self.base_url + '?sensor' +sensor_num_string)
        sensor_tag = 'sensor' + sensor_num_string
        root = ET.fromstring(response.text)
        sensor = root.find(sensor_tag)
        return sensor.text
