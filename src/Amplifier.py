from HardwareSpec import HardwareSpec
class Amplifier:

    def __init__(self):
        self.amplifier_spec	= None
        self.gain = None
        self.noise_figure = None
        self.max_power = None

    def __init__(self, meta):
        if 'amplifier_spec' in meta:
            print('setting amplifier_spec')
            self.amplifier_spec = HardwareSpec(meta['amplifier_spec'])
        if 'gain' in meta:
            self.gain = meta['gain']
        if 'noise_figure' in meta:
            self.noise_figure = meta['noise_figure']
        if 'noise_figure' in meta:
            self.max_power = meta['max_power']
