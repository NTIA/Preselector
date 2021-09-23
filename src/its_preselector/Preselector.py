from its_preselector.RfPath import RfPath
from its_preselector.Filter import Filter
from its_preselector.Amplifier import Amplifier
from its_preselector.CalSource import CalSource
from its_preselector.HardwareSpec import HardwareSpec
import requests


class Preselector:

    def __init__(self):
        self.config = None
        self.rf_paths = []

    def __init__(self, sigmf, config):
        self.config = config
        self.filters = []
        try:
            self._set_filters(sigmf['global']['ntia-sensor:sensor']['preselector']['filters'])
        except KeyError as e:
            pass

        self.amplifiers = []
        try:
            self._set_amplifiers(sigmf['global']['ntia-sensor:sensor']['preselector']['amplifiers'])
        except KeyError as e:
            pass

        self.rf_paths=[]
        try:
            self._get_rf_paths(sigmf['global']['ntia-sensor:sensor']['preselector']['rf_paths'])
        except KeyError as e:
            pass

        self.cal_sources = []
        try:
            self._set_cal_sources(sigmf['global']['ntia-sensor:sensor']['preselector']['cal_sources'])
        except KeyError as e:
            pass

        self.preselector_spec = []
        try:
           self.preselector_spec = HardwareSpec(sigmf['global']['ntia-sensor:sensor']['preselector']['preselector_spec'])
        except KeyError as e:
            pass


    def _get_rf_paths(self, paths):
        for path in paths:
            rf_path = RfPath(path)
            self.rf_paths.append(rf_path)

    def _set_filters(self, filters):
        for f in filters:
            filter = Filter(f)
            self.filters.append(filter)

    def _set_amplifiers(self, amplifiers):
        for a in amplifiers:
            amplifier = Amplifier(a)
            self.amplifiers.append(amplifier)

    def _set_cal_sources(self, cal_sources):
        for c in cal_sources:
            cal_source = CalSource(c)
            self.cal_sources.append(cal_source)

    def get_frequency_low_passband(self, rf_path_index):
        if rf_path_index < len(self.rf_paths):
            path = self.rf_paths[rf_path_index]
            filter_id = path.filter_id
            filter =self._get_filter(filter_id)
            if filter:
                return filter.frequency_low_passband
        return None

    def get_frequency_high_passband(self, rf_path_index):
        if rf_path_index < len(self.rf_paths):
            path = self.rf_paths[rf_path_index]
            filter_id = path.filter_id
            filter = self._get_filter(filter_id)
            if filter:
                return filter.frequency_high_passband
        return None

    def get_frequency_low_stopband(self, rf_path_index):
        if rf_path_index < len(self.rf_paths):
            path = self.rf_paths[rf_path_index]
            filter_id = path.filter_id
            filter = self._get_filter(filter_id)
            if filter:
                return filter.frequency_low_stopband
        return None

    def get_frequency_high_stopband(self, rf_path_index):
        if rf_path_index < len(self.rf_paths):
            path = self.rf_paths[rf_path_index]
            filter_id = path.filter_id
            filter = self._get_filter(filter_id)
            if filter:
                return filter.frequency_high_stopband
        return None

    def get_gain(self, rf_path_index):
        if rf_path_index < len(self.rf_paths):
            path = self.rf_paths[rf_path_index]
            amp_id = path.amplifier_id
            amplifier = self._get_amplifier(amp_id)
            if amplifier:
                return amplifier.gain
        return None

    def get_noise_figure(self, rf_path_index):
        if rf_path_index < len(self.rf_paths):
            path = self.rf_paths[rf_path_index]
            amp_id = path.amplifier_id
            amplifier = self._get_amplifier(amp_id)
            if amplifier:
                return amplifier.noise_figure
        return None

    def set_rf_path_on(self, i):
        switches = self.config[str(i)]['on'].split(',')
        for i in range(len(switches)):
            command = self.config['WEB_RELAY']['base_url'] + switches[i]
            print(command)
            requests.get(command)


    def set_rf_path_off(self, i):
        switches = self.config['WEB_RELAY']['base_url'] + self.config[str(i)]['off'].split(',')
        for i in range(len(switches)):
            command = self.config['WEB_RELAY']['base_url'] + switches[i]
            print(command)
            requests.get(command)

    def set_source_on(self, key):
        switches =  self.config[key]['on'].split(',')
        for i in range(len(switches)):
            command = self.config['WEB_RELAY']['base_url'] + switches[i]
            print(command)
            requests.get(command)



    def set_source_off(self, key):
        switches = self.config[key]['off'].split(',')
        for i in range(len(switches)):
            command = self.config['WEB_RELAY']['base_url'] + switches[i]
            print(command)
            requests.get(command)


    def _get_filter(self, filter_id):
        if filter_id:
            for f in self.filters:
                if f.filter_spec.id == filter_id:
                    return f

        return None


    def _get_amplifier(self, amp_id):
        if amp_id:
            for amp in self.amplifiers:
                if amp.amplifier_spec.id == amp_id:
                    return amp

        return None




