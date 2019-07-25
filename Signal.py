from BaseTools import BasicDevice


class Signal(BasicDevice):
    def __init__(self, width, **kwargs):
        self.width = width
        self.need_high_fanout = False
        self.high_fanout_instantiated = False
