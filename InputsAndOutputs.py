from BaseTools import BasicDevice
from Signal import Signal


class Input(Signal):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class Output(Signal):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class Clock(Signal):
    def __init__(self, **kwargs):
        assert("width" not in kwargs)
        super().__init__(width=1, **kwargs)

    def render_vhdl(self):
        y = []
        if self.my_level == 0:
            # In this case, render the high fanout buffer
            y.append()
        else:
            # In this case, don't:
            y.append()
        return y

    def render_verilog(self):
        y = []
        if self.my_level == 0:
            # In this case, render the high fanout buffer
            y.append()
        else:
            # In this case, don't:
            y.append()
        return y


class BusWidth(BasicDevice):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.width = kwargs["width"]

    def render_vhdl(self):
        pass

    def render_verilog(self):
        pass
