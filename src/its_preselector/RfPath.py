class RfPath:

    def __init__(self, props):
        self.name = None
        self.cal_source_id= props['cal_source_id']
        self.filter_id = props['filter_id']
        self.amplifier_id = props['amplifier_id']
        if 'name' in props:
            self.name = props['name']

