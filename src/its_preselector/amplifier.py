from its_preselector.hardware_spec import HardwareSpec


class Amplifier:
    def __init__(self, meta):
        self.amplifier_spec = None
        self.gain = None
        self.noise_figure = None
        self.max_power = None
        if "amplifier_spec" in meta:
            self.amplifier_spec = HardwareSpec(meta["amplifier_spec"])
        if "gain" in meta:
            self.gain = meta["gain"]
        if "noise_figure" in meta:
            self.noise_figure = meta["noise_figure"]
        if "max_power" in meta:
            self.max_power = meta["max_power"]
