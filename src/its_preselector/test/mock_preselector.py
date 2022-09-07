from its_preselector.preselector import Preselector


class MockPreselector(Preselector):

    def __init__(self):
        self.id = "mock"
        self.name = "mock_preselector"

    def set_state(self, state_name: str) -> None:
        """
        Sets the state of the preselector.
        :param state_name: The name of the state (config key value) to enable in the preselector.
        """
        return

    def get_sensor_value(self, sensor) -> str:
        """
        Read the value from a sensor on the preselector.
        :param sensor: The name or id of the sensor.
        :return: The string value of from the sensor,  e.g. the temperature.
        """
        return ""

    @property
    def id(self) -> str:
        """
        The id of the preselector.
        :return: The id of the preselector.
        """
        return self.id

    @property
    def name(self) -> str:
        """
        Get the name of the preselector.
        :return: The name of the preselector.
        """
        return self.name

    def get_status(self) -> dict:
        """
        Get the status of the preselector. The status dictionary should include a name
        key value pair indicating the name of hte preselector, a healthy key that maps to
        a boolean field to indicate if the preselector is healthy, and any number of additional
        keys that map to boolean status values to indicate if the states are enabled or not.
        :return: A dictionary representing the status of the preselector.
        """
        return {
            "name": self.name,
            "healthy": True
        }