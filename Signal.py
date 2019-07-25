from BaseTools import BasicDevice


class Signal(BasicDevice):
    def __init__(self, width, **kwargs):
        self.width = width
        self.need_high_fanout = False
        self.high_fanout_instantiated = False

    def render_declaration_vhdl(self):
        pass

    def render_declaration_verilog(self):
        pass

    def render_verilog(self):
        pass

    def render_vhdl(self):
        pass
