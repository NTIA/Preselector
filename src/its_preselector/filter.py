from its_preselector.hardware_spec import HardwareSpec


class Filter:

    def __init__(self, props):
        self.filter_spec = None
        self.frequency_low_passband = None
        self.frequency_high_passband = None
        self.frequency_low_stopband = None
        self.frequency_high_stopband = None
        if 'filter_spec' in props:
            self.filter_spec = HardwareSpec(props['filter_spec'])
        if 'frequency_low_passband' in props:
            self.frequency_low_passband = props['frequency_low_passband']
        if 'frequency_high_passband' in props:
            self.frequency_high_passband = props['frequency_high_passband']
        if 'frequency_low_stopband' in props:
            self.frequency_low_stopband = props['frequency_low_stopband']
        if 'frequency_high_stopband' in props:
            self.frequency_high_stopband = props['frequency_high_stopband']
