from its_preselector.HardwareSpec import HardwareSpec
class CalSource:

    def __init__(self, props):
        self.cal_source_spec = None
        self.type = None
        self.enr = None
        if 'cal_source_spec' in props:
            self.cal_source_spec = HardwareSpec(props['cal_source_spec'])
        if 'type' in props:
            self.type = props['type']
        if 'enr' in props:
            self.enr = props['enr']