from BaseTools import BasicDevice


class Entity(BasicDevice):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.signals = []
        self.components = []
        self.port_maps = []

    def render_declaration_vhdl(self):
        raise NotImplemented()

    def render_declaration_verilog(self):
        raise NotImplemented()

    def render_port_map_vhdl(self):
        raise NotImplemented()

    def render_port_map_verilog(self):
        raise NotImplemented()

    def render_module_vhdl(self):
        """Includes entity declaration"""
        raise NotImplemented()

    def render_module_verilog(self):
        raise NotImplemented()

    def render(self):
        raise NotImplemented
        # TODO: if level == 0,
        #   1) Double buffer all ins/outs,
        #   2) Route all clocks & resets through high fanout buffers
