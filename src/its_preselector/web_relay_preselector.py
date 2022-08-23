import logging

from its_preselector.configuration_exception import ConfigurationException
from its_preselector.controlbyweb_web_relay import ControlByWebWebRelay
from its_preselector.preselector import Preselector

logger = logging.getLogger(__name__)


class WebRelayPreselector(Preselector):

    def __init__(self, sigmf: dict, config: dict):
        super().__init__(sigmf, config)
        self.web_relay = ControlByWebWebRelay(config)

    def set_state(self, state_name: str):
        self.web_relay.set_state(i)

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
