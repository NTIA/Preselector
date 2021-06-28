class HardwareSpec:

    def __init__(self):
        self.id=None
        self.model = None
        self.version = None
        self.supplemental_information = None

    def __init__(self, props):
        if 'id' in props:
            self.id = props['id']
        if 'model' in props:
            self.model = None
        if 'supplemental_information' in props:
            self.supplemental_information = None
        if 'version' in props:
            self.version = props['version']
