from BaseTools import BasicDevice
from WhiteSpaceTools import whitespace


class Generic(BasicDevice):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        kind = kwargs["kind"]
        assert(kind == "int" or kind == "time")
        self.kind = kind
        if "default" in kwargs:
            self.default = kwargs["default"]
        else:
            self.default = None

    def declare_vhdl(self):
        y = ""
        y += self.name
        y += whitespace(2)
        y += ":"
        y += whitespace(2)
        if self.kind == "int":
            y += "integer"
        else:
            y += "time"
        if self.default is not None:
            y += " := " + str(self.default)
        return [y]

    def declare_verilog(self):
        pass

    def render_verilog(self):
        return []

    def render_vhdl(self):
        return []

    def __str__(self):
        return self.name


if __name__ == "__main__":
    uut1 = Generic(name="MY_GENERIC", kind="int", default=42)
    print(uut1.declare_vhdl()[0])
    uut2 = Generic(name="ANOTHER_GENERIC", kind="int")
    print(uut2.declare_vhdl()[0])
    uut3 = Generic(name="GENERIC_3", kind="time", default="1 ns")
    print(uut3.declare_vhdl()[0])
