from DataTypes import basic_signal
from Signal import Signal
from WhiteSpaceTools import whitespace


class Input(Signal):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def declare_vhdl(self):
        y = ""
        y += self.name
        y += whitespace(2)
        y += ":"
        y += whitespace(3)
        y += "in"
        y += whitespace(3)
        y += basic_signal(self.width)
        y += ";"
        return [y]


class Output(Signal):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def declare_vhdl(self):
        y = ""
        y += self.name
        y += whitespace(2)
        y += ":"
        y += whitespace(2)
        y += "out"
        y += whitespace(2)
        y += basic_signal(self.width)
        y += ";"
        return [y]
