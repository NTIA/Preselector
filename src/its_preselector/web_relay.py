from abc import ABC, abstractmethod


class WebRelay(ABC):
    def __init__(self, config):
        self.config = config


@abstractmethod
def get_sensor_value(sensor):
    pass


@abstractmethod
def set_state(self, i):
    pass


@abstractmethod
def healthy(self):
    pass
