class RfPath:

    def __init__(self, props):
        self.name = None
        if 'cal_source_id' in props:
            self.cal_source_id = props['cal_source_id']
        if 'filter_id' in props:
            self.filter_id = props['filter_id']
        if 'amplifier_id' in props:
            self.amplifier_id = props['amplifier_id']
        if 'name' in props:
            self.name = props['name']

