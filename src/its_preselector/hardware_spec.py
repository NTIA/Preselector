class HardwareSpec:

    def __init__(self, props):
        self.id=None
        self.model = None
        self.version = None
        self.supplemental_information = None
        if 'id' in props:
            self.id = props['id']
        if 'model' in props:
            self.model = props['model']
        if 'supplemental_information' in props:
            self.supplemental_information = props['supplemental_information']
        if 'version' in props:
            self.version = props['version']
