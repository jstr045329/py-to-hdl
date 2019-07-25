from BaseTools import BasicDevice


class Entity(BasicDevice):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

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
