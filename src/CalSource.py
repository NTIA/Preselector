class CalSource:

    def __init__(self):
        self.cal_source_spec = None
        self.type = None
        self.enr = None

    def __init__(self, props):
        if 'cal_source_spec' in props:
            self.cal_source_spec = props['cal_source_spec']
        if 'type' in props:
            self.type = props['type']
        if 'enr' in props:
            self.enr = props['enr']