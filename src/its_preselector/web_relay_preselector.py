import logging
from its_preselector.controlbyweb_web_relay import ControlByWebWebRelay
from its_preselector.preselector import Preselector


logger = logging.getLogger(__name__)


class WebRelayPreselector(Preselector):

    def __init__(self, sigmf, config):
        super().__init__(sigmf, config)
        self.web_relay = ControlByWebWebRelay(config)

    def set_state(self, i):
        self.web_relay.set_state(i)

    def get_sensor_value(self, sensor_num):
        return self.web_relay.get_sensor_value(sensor_num)

    def healthy(self):
        return self.web_relay.healthy()
