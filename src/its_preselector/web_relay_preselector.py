import logging
from its_preselector.preselector import Preselector
import requests
import xml.etree.ElementTree as ET

logger = logging.getLogger(__name__)


class WebRelayPreselector(Preselector):

    def __init__(self, sigmf, config):
        super().__init__(sigmf, config)
        if 'base_url' in config:
            self.base_url = config['base_url']

    def set_state(self, i):
        key = str(i)
        if key in self.config:
            switches = self.config[str(i)].split(',')
            if self.base_url and self.base_url != '':
                for i in range(len(switches)):
                    command = self.base_url + '?relay' + switches[i]
                    logger.debug(command)
                    response = requests.get(command)
                    if response.status_code != requests.codes.ok:
                        raise Exception('Unable to set preselector state. Verify configuration and connectivity.')
            else:
                raise Exception('base_url is None or blank')
        else:
            raise Exception("RF path " + key + " configuration does not exist.")

    def get_sensor_value(self, sensor_num):
        sensor_num_string = str(sensor_num)
        response = requests.get(self.base_url + '?sensor' + sensor_num_string)
        sensor_tag = 'sensor' + sensor_num_string
        root = ET.fromstring(response.text)
        sensor = root.find(sensor_tag)
        return sensor.text

    def healthy(self):
        try:
            response = requests.get(self.base_url)
            return response.status_code == requests.codes.ok
        except:
            logger.error("Unable to connect to preselector")
        return False
