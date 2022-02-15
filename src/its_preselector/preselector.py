from abc import ABC, abstractmethod
from its_preselector.rf_path import RfPath
from its_preselector.filter import Filter
from its_preselector.amplifier import Amplifier
from its_preselector.cal_source import CalSource
from its_preselector.hardware_spec import HardwareSpec


class Preselector(ABC):

    config = None
    base_url = None
    amplifiers = []
    rf_paths = []
    filters = []
    cal_sources = []
    preselector_spec = []

    def __init__(self):
        pass

    def __init__(self, sigmf, config):
        self.config = config
        if 'WEB_RELAY' in config:
            web_relay = self.config['WEB_RELAY']
            if 'base_url' in web_relay:
                self.base_url = web_relay['base_url']
        try:
            self.__set_filters(sigmf['global']['ntia-sensor:sensor']['preselector']['filters'])
        except KeyError:
            pass

        try:
            self.__set_amplifiers(sigmf['global']['ntia-sensor:sensor']['preselector']['amplifiers'])
        except KeyError:
            pass

        try:
            self.__get_rf_paths(sigmf['global']['ntia-sensor:sensor']['preselector']['rf_paths'])
        except KeyError:
            pass

        try:
            self.__set_cal_sources(sigmf['global']['ntia-sensor:sensor']['preselector']['cal_sources'])
        except KeyError:
            pass

        try:
            self.preselector_spec = HardwareSpec(
                sigmf['global']['ntia-sensor:sensor']['preselector']['preselector_spec'])
        except KeyError:
            pass
        self.__add_sources()

    def __get_rf_paths(self, paths):
        for path in paths:
            rf_path = RfPath(path)
            self.rf_paths.append(rf_path)

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

    def get_frequency_low_passband(self, rf_path_index):
        if rf_path_index < len(self.rf_paths):
            path = self.rf_paths[rf_path_index]
            filter_id = path.filter_id
            preselctor_filter = self.__get_filter(filter_id)
            if preselctor_filter:
                return preselctor_filter.frequency_low_passband
        return None

    def get_frequency_high_passband(self, rf_path_index):
        if rf_path_index < len(self.rf_paths):
            path = self.rf_paths[rf_path_index]
            filter_id = path.filter_id
            preselector_filter = self.__get_filter(filter_id)
            if preselector_filter:
                return preselector_filter.frequency_high_passband
        return None

    def get_frequency_low_stopband(self, rf_path_index):
        if rf_path_index < len(self.rf_paths):
            path = self.rf_paths[rf_path_index]
            filter_id = path.filter_id
            preselector_filter = self.__get_filter(filter_id)
            if preselector_filter:
                return preselector_filter.frequency_low_stopband
        return None

    def get_frequency_high_stopband(self, rf_path_index):
        if rf_path_index < len(self.rf_paths):
            path = self.rf_paths[rf_path_index]
            filter_id = path.filter_id
            preselctor_filter = self.__get_filter(filter_id)
            if preselctor_filter:
                return preselctor_filter.frequency_high_stopband
        return None

    def get_amplifier_gain(self, rf_path_index):
        if rf_path_index < len(self.rf_paths):
            path = self.rf_paths[rf_path_index]
            amp_id = path.amplifier_id
            amplifier = self.__get_amplifier(amp_id)
            if amplifier:
                return amplifier.gain
        return None

    def get_amplifier_noise_figure(self, rf_path_index):
        if rf_path_index < len(self.rf_paths):
            path = self.rf_paths[rf_path_index]
            amp_id = path.amplifier_id
            amplifier = self.__get_amplifier(amp_id)
            if amplifier:
                return amplifier.noise_figure
        return None

    @abstractmethod
    def set_rf_path(self, i):
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

    def __add_sources(self):
        if self.rf_paths:
            for i in range(len(self.rf_paths)):
                rf_path = self.rf_paths[i]
                if rf_path.name:
                    if rf_path.name not in self.config:
                        path = self.config[str(i)]
                        self.config[rf_path.name] = path


