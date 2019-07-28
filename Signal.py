from BaseTools import BasicDevice
from WhiteSpaceTools import whitespace
from DataTypes import basic_signal
from ParseExpression import parse_expression


class Signal(BasicDevice):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if "width" in kwargs:
            self.width = kwargs["width"]
            assert(self.width >= 1)
        else:
            self.width = 1

        # Set this to true for clks/resets that should not go through high fanout:
        self.enable_high_fanout = True
        self.force_high_fanout = False
        self.expression = kwargs["expression"]

    def disable_high_fanout(self):
        self.enable_high_fanout = False

    def use_high_fanout(self):
        """Detects """
        if self.force_high_fanout:
            return True
        elif self.enable_high_fanout:
            return ("clk" in self.name or
                    "clock" in self.name or
                    "rst" in self.name or
                    "reset" in self.name)
        else:
            return False

    def declare_vhdl(self):
        y = ""
        y += "signal"
        y += whitespace(6)
        y += self.name
        y += whitespace(2)
        y += ":"
        y += whitespace(2)
        y += basic_signal()
        y += "("
        y += str(self.width-1)
        y += " downto 0);"
        return [y]

    def declare_verilog(self):
        pass

    def render_verilog(self):
        pass

    def render_vhdl(self):
        y = ""
        y += self.name
        y += " <= "
        y += parse_expression(self.expression)
        return [y]


if __name__ == "__main__":
    uut = Signal(width=1, target_lang="vhdl", name="mySignal", expression="joe && harry || !fred")
    for m in uut.declare_vhdl():
        print(m)
    for m in uut.render():
        print(m)





