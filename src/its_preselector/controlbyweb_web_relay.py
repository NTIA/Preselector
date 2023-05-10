import asyncio
import logging

import defusedxml.ElementTree as ET
import httpx

from its_preselector.configuration_exception import ConfigurationException
from its_preselector.web_relay import WebRelay

logger = logging.getLogger(__name__)


class ControlByWebWebRelay(WebRelay):
    def __init__(self, config: dict, timeout: int = 1, retries=3):
        """
        :param config: The web relay configuration dictionary. The dictionary must
        include "name" and "base_url" entries.
        :param timeout: The timeout in seconds that will be used in any web requests.
        :param retries: The total number of retry attempts to make in the event of a failure to set_state, get_sensor_value, or check health.
        """
        super().__init__(config, timeout)
        if "base_url" not in config:
            raise ConfigurationException("Config must include base_url.")
        elif config["base_url"] is None:
            raise ConfigurationException("base_url cannot be None.")
        elif config["base_url"] == "":
            raise ConfigurationException("base_url cannot be blank.")
        else:
            self.base_url = config["base_url"]
        if self.base_url.endswith("/"):
            self.base_url = self.base_url[:-1]
        if "name" not in config:
            raise ConfigurationException("Config must include name.")
        elif config["name"] is None:
            raise ConfigurationException("name cannot be None.")
        elif config["name"] == "":
            raise ConfigurationException("name cannot be blank.")
        self.retries = retries
        self.http_transport = httpx.HTTPTransport(retries=self.retries)
        self.http_client = httpx.AsyncClient(
            base_url=self.base_url, timeout=self.timeout, transport=self.http_transport
        )
        self.loop = asyncio.get_event_loop()

    def __del__(self):
        """
        Destructor method should help close the client and event loop at exit.
        """
        self.loop.run_until_complete(self.close_client())
        self.loop.close()

    async def close_client(self):
        await self.http_client.close()

    def get_sensor_value(self, sensor_num: int) -> float:
        """
        Read numeric value from a 1-Wire sensor of the WebRelay.

        :param sensor_num: Configured index of the desired sensor.
        :raises ConfigurationException: If the requested sensor cannot be read.
        :return: The desired sensor value.
        """
        sensor_num_string = str(sensor_num)
        response = self.request_with_retry()
        # Check for X310 xml format first.
        sensor_tag = "sensor" + sensor_num_string
        root = ET.fromstring(response.text)
        sensor = root.find(sensor_tag)
        if sensor is None:
            # Didn't find X310 format sensor so check for X410 format.
            sensor_tag = "oneWireSensor" + sensor_num_string
            sensor = root.find(sensor_tag)
        if sensor is None:
            raise ConfigurationException(f"Sensor {sensor_num} does not exist.")
        return float(sensor.text)

    def get_digital_input_value(self, input_num: int) -> bool:
        """
        Read boolean value from a digital input of the WebRelay.

        A value of ``False`` is returned if the digital input is not
        configured, since the XML response includes a zero for any
        digital inputs which exist but are not configured.

        :param input_num: Configured index of the desired digital input.
        :return: The boolean value of the desired digital input.
        """
        input_num = int(input_num)
        response = self.request_with_retry()
        # Check for X310 format first
        input_tag = f"input{input_num}state"
        root = ET.fromstring(response.text)
        digital_input = root.find(input_tag)
        if digital_input is None:
            # Didn't find X310 format, check for X410 format
            input_tag = f"digitalInput{input_num}"
            digital_input = root.find(input_tag)
        if digital_input is None:
            raise ConfigurationException(f"Digital Input {input_num} does not exist.")
        return bool(int(digital_input.text))

    def set_state(self, key):
        """
        Set the state of the relay.
        :param key: The key for the desired state or states as defined in the config.
        :return: None
        :raises httpx.ConnectTimeout: If the program is unable to connect
            to the preselector before the configured timeout interval passes.
        """
        if key in self.config["control_states"]:
            switches = self.config["control_states"][str(key)].split(",")
            if self.base_url and self.base_url != "":
                for s in switches:
                    params = {f"?relay{s.split('=')[0]}": s.split("=")[1]}
                    logger.debug(self.base_url, params)
                    response = self.request_with_retry(params)
                    if response.status_code != httpx.codes.OK:
                        raise Exception(
                            "Unable to set preselector state. Verify configuration and connectivity."
                        )
            else:
                raise Exception("base_url is None or blank")
        else:
            raise Exception(f"RF path {key} configuration does not exist.")

    def healthy(self) -> bool:
        """
        Check if the relay can be reached.
        :return: True if the relay can be reached, or False if it cannot be reached.
        """
        try:
            response = self.request_with_retry()
            return response.status_code == httpx.codes.OK
        except:
            logger.error("Unable to connect to preselector")
        return False

    @property
    def id(self):
        return self.base_url

    @property
    def name(self):
        return self.config["name"]

    def get_status(self):
        state = {}
        healthy = False
        try:
            response = self.get_state_xml()
            logger.debug(f"status code: {response.status_code}")
            healthy = response.status_code == httpx.codes.OK
            if healthy:
                state_xml = response.text
                xml_root = ET.fromstring(state_xml)

                for key, value in self.config["status_states"].items():
                    relay_states = value.split(",")
                    matches = True
                    for relay_state in relay_states:
                        matches = matches and self.state_matches(relay_state, xml_root)
                    state[key] = matches
        except:
            logger.error("Unable to get status")
        state["healthy"] = healthy
        state["name"] = self.name
        return state

    def state_matches(self, relay_and_state, xml_root):
        relay_state_list = relay_and_state.split("=")
        desired_state = relay_state_list[1]
        relay_tag = relay_state_list[0]
        relay_element = xml_root.find(relay_tag)
        if relay_element is None:
            raise Exception("Unable to locate " + relay_tag)
        else:
            return desired_state == relay_element.text

    def get_state_summary(self, response):
        relay_state = (
            "1State="
            + self.get_relay_state(response, "relay1")
            + ",2State="
            + self.get_relay_state(response, "relay2")
            + ",3State="
            + self.get_relay_state(response, "relay3")
            + ",4State="
            + self.get_relay_state(response, "relay4")
        )
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
            raise Exception(f"Relay {relay} does not exist.")
        else:
            relay_state = relay_node.text
            if relay_state == "1":
                return True
            else:
                return False

    @staticmethod
    def get_relay_state(state_xml, relay):
        root = ET.fromstring(state_xml)
        relay_node = root.find(relay)
        if relay_node is None:
            raise Exception(f"Relay {relay} does not exist.")
        else:
            relay_state = relay_node.text
            return relay_state

    def get_state_xml(self):
        if self.base_url and self.base_url != "":
            response = self.request_with_retry()
            return response
        else:
            raise Exception("base_url is None or blank")

    def request_with_retry(self, params: dict = None) -> httpx.Response:
        return self.loop.run_until_complete(self.__async__request_with_retry(params))

    async def __async__request_with_retry(self, params: dict = None) -> httpx.Response:
        async with self.http_client as client:
            response = await client.get(params=params)
        return response
