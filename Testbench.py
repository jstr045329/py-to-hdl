from BaseTools import BasicDevice


class Testbench(BasicDevice):
    def __init__(self, **kwargs):
        super().__init__(parent=None, **kwargs)
