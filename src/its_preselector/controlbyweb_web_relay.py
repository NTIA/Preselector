from its_preselector.web_relay import WebRelay
import logging
import requests
import xml.etree.ElementTree as ET

logger = logging.getLogger(__name__)


class ControlByWebWebRelay(WebRelay):

    def __init__(self, config):
        super().__init__(config)
        if 'base_url' in config:
            self.base_url = config['base_url']

    def get_sensor_value(self, sensor_num):
        sensor_num_string = str(sensor_num)
        response = requests.get(self.base_url)
        # Check for X310 xml format first.
        sensor_tag = 'sensor' + sensor_num_string
        root = ET.fromstring(response.text)
        sensor = root.find(sensor_tag)
        if sensor is None:
            # Didn't find X310 format sensor so check for X410 format.
            sensor_tag = 'oneWireSensor' + sensor_num_string
            sensor = root.find(sensor_tag)
        if sensor is None:
            return None
        else:
            return sensor.text

    def set_state(self, key):
        if key in self.config['control_states']:
            switches = self.config['control_states'][str(key)].split(',')
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

    def healthy(self):
        try:
            response = requests.get(self.base_url)
            return response.status_code == requests.codes.ok
        except:
            logger.error("Unable to connect to preselector")
        return False

    @property
    def id(self):
        return self.base_url

    @property
    def name(self):
        return self.config['name']

    def get_status(self):
        state = {}
        healthy = False
        try:
            response = self.get_state_xml()
            logger.debug('status code: ' + str(response.status_code))
            healthy = response.status_code == requests.codes.ok
            if healthy:
                state_xml = response.text
                xml_root = ET.fromstring(state_xml)

                for key, value in self.config['status_states'].items():
                    relay_states = value.split(',')
                    matches = True
                    for relay_state in relay_states:
                        matches = matches and self.state_matches(relay_state, xml_root)
                    state[key] = matches
        except:
            logger.error('Unable to get status')
        state['healthy'] = healthy
        state['name'] = self.name
        return state

    def state_matches(self, relay_and_state, xml_root):
        relay_state_list = relay_and_state.split('=')
        desired_state = relay_state_list[1]
        relay_tag = relay_state_list[0]
        relay_element = xml_root.find(relay_tag)
        if relay_element is None:
            raise Exception('Unable to locate ' + relay_tag)
        else:
            return desired_state == relay_element.text

    def get_state_summary(self, response):
        relay_state = '1State=' + self.get_relay_state(response, 'relay1') + \
                      ',2State=' + self.get_relay_state(response, 'relay2') + \
                      ',3State=' + self.get_relay_state(response, 'relay3') + \
                      ',4State=' + self.get_relay_state(response, 'relay4')
        return relay_state

    def map_relay_state_to_config(self, relay_state):
        for k, value in self.config.items():
            if relay_state == value:
                return k
        return None

    @staticmethod
    def is_enabled(state_xml, relay):
        root = ET.fromstring(state_xml)
        relay_node = root.find(relay)
        if relay_node is None:
            raise Exception('Relay ' + relay + ' does not exist.')
        else:
            relay_state = relay_node.text
            if relay_state == '1':
                return True
            else:
                return False

    @staticmethod
    def get_relay_state(state_xml, relay):
        root = ET.fromstring(state_xml)
        relay_node = root.find(relay)
        if relay_node is None:
            raise Exception('Relay ' + relay + ' does not exist.')
        else:
            relay_state = relay_node.text
            return relay_state

    def get_state_xml(self):
        if self.base_url and self.base_url != '':
            response = requests.get(self.base_url, timeout=1)
            return response
        else:
            raise Exception('base_url is None or blank')
