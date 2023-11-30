from abc import ABC, abstractmethod


class WebRelay(ABC):
    def __init__(self, config: dict, timeout: int = 1):
        """
        :param config: The web relay configuration dictionary.
        :param timeout: The timeout in seconds that will be used in any web requests.
        """
        self.config = config
        self.timeout = timeout

    @abstractmethod
    def get_sensor_value(self, sensor) -> float:
        """
        Read the value from a 1-Wire sensor on the web relay.

        :param sensor: The ID of the sensor.
        :return: The float value read from the sensor, e.g. the temperature.
        """
        pass

    @abstractmethod
    def get_digital_input_value(self, input_id) -> bool:
        """
        Read the value from a digital input on the web relay.

        :param input_id: The ID of the digital input
        :return: The boolean value read from the digital input.
        """

    @abstractmethod
    def get_analog_input_value(self, input_id) -> float:
        """
        Read the value from an analog input on the web relay.

        :param input_id: The ID of the analog input
        :return: The float value read from the analog input.
        """

    @abstractmethod
    def set_state(self, state_key: str) -> None:
        """
        Set the state of the web relay as defined in the config.
        :param state_key: The key from the config that maps to the desired web relay states.
        :return: None
        """
        pass

    @abstractmethod
    def healthy(self) -> bool:
        """
        Method to determine if the web relay is healthy.
        :return: True if the web relay is healthy. False if it is not.
        """
        pass

    @property
    @abstractmethod
    def id(self) -> str:
        """
        Get the unique id of hte web relay.
        :return: The unique string id of the web relay.
        """
        pass

    @property
    @abstractmethod
    def name(self) -> str:
        """
        Get the name of the web relay.
        :return: The string name of the web relay.
        """
        pass

    @abstractmethod
    def get_status(self) -> dict:
        """
        Get the status of the web relay.
        :return: A dict describing the status of the web relay. The dict should include a 'name' key that maps to the
        name of the web relay, a 'healthy' key that maps to the value returned from healthy(), and any keys defined in
        the config that map to boolean values indicating whether or not those states are enabled.
        """
        pass
