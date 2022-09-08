import logging

from its_preselector.configuration_exception import ConfigurationException
from its_preselector.controlbyweb_web_relay import ControlByWebWebRelay
from its_preselector.preselector import Preselector

logger = logging.getLogger(__name__)


class WebRelayPreselector(Preselector):
    def __init__(self, sensor_definition: dict, config: dict, timeout: int = 1):
        """
        :param sensor_definition: JSON representation of the sensor definition including the preselector. The
        sensor_definition may be SigMF that includes the sensor definition as specified in
        https://github.com/NTIA/sigmf-ns-ntia, or it may be only the Sensor JSON.
        :param config: The preselector configuration dictionary.
        :param timeout: The timeout in seconds that will be used in any web requests.
        """
        super().__init__(sensor_definition, config)
        self.web_relay = ControlByWebWebRelay(config, timeout)

    def set_state(self, state_name: str):
        self.web_relay.set_state(state_name)

    def get_sensor_value(self, sensor_num) -> str:
        return self.web_relay.get_sensor_value(sensor_num)

    def healthy(self) -> bool:
        return self.web_relay.healthy()

    @property
    def id(self):
        return self.web_relay.base_url

    @property
    def name(self):
        return self.web_relay.name

    def get_status(self):
        return self.web_relay.get_status()
