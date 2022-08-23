from abc import ABC, abstractmethod

from its_preselector.configuration_exception import ConfigurationException
from its_preselector.rf_path import RfPath
from its_preselector.filter import Filter
from its_preselector.amplifier import Amplifier
from its_preselector.cal_source import CalSource
from its_preselector.hardware_spec import HardwareSpec


class Preselector(ABC):

    def __init__(self, sigmf: dict, config: dict):
        self.amplifiers = []
        self.rf_paths = {}
        self.filters = []
        self.cal_sources = []
        self.preselector_spec = []
        self.config = config
        try:
            if 'global' in sigmf:
                self.__set_filters(sigmf['global']['ntia-sensor:sensor']['preselector']['filters'])
            else:
                self.__set_filters(sigmf['preselector']['filters'])
        except KeyError:
            pass

        try:
            if 'global' in sigmf:
                self.__set_amplifiers(sigmf['global']['ntia-sensor:sensor']['preselector']['amplifiers'])
            else:
                self.__set_amplifiers(sigmf['preselector']['amplifiers'])
        except KeyError:
            pass

        try:
            if 'global' in sigmf:
                self.__get_rf_paths(sigmf['global']['ntia-sensor:sensor']['preselector']['rf_paths'])
            else:
                self.__get_rf_paths(sigmf['preselector']['rf_paths'])
        except KeyError:
            pass

        try:
            if 'global' in sigmf:
                self.__set_cal_sources(sigmf['global']['ntia-sensor:sensor']['preselector']['cal_sources'])
            else:
                self.__set_cal_sources(sigmf['preselector']['cal_sources'])
        except KeyError:
            pass

        try:
            if 'global' in sigmf:
                self.preselector_spec = HardwareSpec(
                    sigmf['global']['ntia-sensor:sensor']['preselector']['preselector_spec'])
            else:
                self.preselector_spec = HardwareSpec(
                    sigmf['preselector']['preselector_spec'])
        except KeyError:
            pass

    def __get_rf_paths(self, paths):
        for path in paths:
            rf_path = RfPath(path)
            self.rf_paths[rf_path.name] = rf_path

    def __set_filters(self, filters):
        for f in filters:
            preselector_filter = Filter(f)
            self.filters.append(preselector_filter)

    def __set_amplifiers(self, amplifiers):
        for a in amplifiers:
            amplifier = Amplifier(a)
            self.amplifiers.append(amplifier)

    def __set_cal_sources(self, cal_sources):
        for c in cal_sources:
            cal_source = CalSource(c)
            self.cal_sources.append(cal_source)

    def get_frequency_low_passband(self, rf_path_name: str) -> float:
        """
         Get the low frequency of the 1 dB passband.
        :param rf_path_name, or name of the rf_path:
        :return:The low frequency of hte 1dB passband in Hz.
        """
        if rf_path_name in self.rf_paths:
            path = self.rf_paths[rf_path_name]
            filter_id = path.filter_id
            preselector_filter = self.__get_filter(filter_id)
            if preselector_filter:
                return preselector_filter.frequency_low_passband
        else:
            raise ConfigurationException(
                "Unable to get frequency_low for the passband filter. There is no RF_PATH named {path_name}".format(
                    path_name=rf_path_name))

    def get_frequency_high_passband(self, rf_path_name: str) -> float:
        """
        Get the high frequency of the 1 dB passband.
        :param rf_path_name: The name of the rf_path.
        :return: The high frequency of the 1 dB passband in Hz.
        """
        if rf_path_name in self.rf_paths:
            path = self.rf_paths[rf_path_name]
            filter_id = path.filter_id
            preselector_filter = self.__get_filter(filter_id)
            if preselector_filter:
                return preselector_filter.frequency_high_passband
        else:
            raise ConfigurationException(
                "Unable to get frequency_high for the passband filter. There is no RF_PATH named {path_name}".format(
                    path_name=rf_path_name))

    def get_frequency_low_stopband(self, rf_path_name: str):
        """
        Gets the low frequency of the 60 dB stopband.
        :param rf_path_name: the name of the rf_path.
        :return: The low frequency of the 60 dB stopband in Hz.
        """
        if rf_path_name in self.rf_paths:
            path = self.rf_paths[rf_path_name]
            filter_id = path.filter_id
            preselector_filter = self.__get_filter(filter_id)
            if preselector_filter:
                return preselector_filter.frequency_low_stopband
        else:
            raise ConfigurationException(
                "Unable to get frequency_low for the stopband filter. There is no RF_PATH named {path_name}".format(
                    path_name=rf_path_name))

    def get_frequency_high_stopband(self, rf_path_name: str) -> float:
        """
        Get the high frequency of the 60 dB stopband.
        :param rf_path_name:
        :return: The high frequency of the 60 dB stopband in Hz.
        """
        if rf_path_name in self.rf_paths:
            path = self.rf_paths[rf_path_name]
            filter_id = path.filter_id
            preselector_filter = self.__get_filter(filter_id)
            if preselector_filter:
                return preselector_filter.frequency_high_stopband
        else:
            raise ConfigurationException(
                "Unable to get frequency_high for the stopband filter. There is no RF_PATH named {path_name}".format(
                    path_name=rf_path_name))

    def get_amplifier_gain(self, rf_path_name: str) -> float:
        """
        Get the gain of the amplifier in the specified rf_path.
        :param rf_path_name:
        :return:
        """
        if rf_path_name in self.rf_paths:
            path = self.rf_paths[rf_path_name]
            amp_id = path.amplifier_id
            amplifier = self.__get_amplifier(amp_id)
            if amplifier:
                return amplifier.gain
        else:
            raise ConfigurationException(
                "Unable to get amplifier gain. There is no RF_PATH named {path_name}".format(
                    path_name=rf_path_name))

    def get_amplifier_noise_figure(self, rf_path_name: str) -> float:
        """
        Get the noise figure of the amplifier in the specified rf_path.
        :param rf_path_name: The name of the rf_path.
        :return: the noise figure of the amplifier in the specified rf_path.
        """
        if rf_path_name in self.rf_paths:
            path = self.rf_paths[rf_path_name]
            amp_id = path.amplifier_id
            amplifier = self.__get_amplifier(amp_id)
            if amplifier:
                return amplifier.noise_figure
        else:
            raise ConfigurationException(
                "Unable to get amplifier noise figure. There is no RF_PATH named {path_name}".format(
                    path_name=rf_path_name))

    @abstractmethod
    def set_state(self, state_name: str) -> None:
        """
        Sets the state of the preselector.
        :param state_name: The name of the state (config key value) to enable in the preselector.
        """
        pass

    def __get_filter(self, filter_id):
        if filter_id:
            for f in self.filters:
                if f.filter_spec.id == filter_id:
                    return f

        return None

    def __get_amplifier(self, amp_id):
        if amp_id:
            for amp in self.amplifiers:
                if amp.amplifier_spec.id == amp_id:
                    return amp

        return None

    @abstractmethod
    def get_sensor_value(self, sensor) -> str:
        """
        Read the value from a sensor on the preselector.
        :param sensor: The name or id of the sensor.
        :return: The string value of from the sensor,  e.g. the temperature.
        """
        pass

    @property
    @abstractmethod
    def id(self) -> str:
        """
        The id of the preselector.
        :return: The id of the preselector.
        """
        pass

    @property
    @abstractmethod
    def name(self) -> str:
        """
        Get the name of the preselector.
        :return: The name of the preselector.
        """
        pass

    @abstractmethod
    def get_status(self) -> dict:
        """
        Get the status of the preselector. The status dictionary should include a name
        key value pair indicating the name of hte preselector, a healthy key that maps to
        a boolean field to indicate if the preselector is healthy, and any number of additional
        keys that map to boolean status values to indicate if the states are enabled or not.
        :return: A dictionary representing the status of the preselector.
        """
        pass
