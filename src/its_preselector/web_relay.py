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

    @property
    @abstractmethod
    def id(self):
        pass

    @property
    @abstractmethod
    def name(self):
        pass

    @abstractmethod
    def get_status(self):
        pass
