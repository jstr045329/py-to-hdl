from BaseTools import BasicDevice
from WhiteSpaceTools import whitespace
from DataTypes import basic_signal
from LiteralTools import bin_literal
from LiteralTools import hex_literal
from LiteralTools import all_ones_binary
from LiteralTools import all_ones_hex

class Generic(BasicDevice):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        kind = kwargs["kind"]
        assert(kind == "int" or kind == "time" or kind == "std_logic" or kind == "std_ulogic")
        if kind == "std_logic" or kind == "std_ulogic":
            self.width = kwargs["width"]
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
        elif self.kind == "std_logic":
            y += "std_logic_vector("
            y += str(self.width-1) + " downto 0)"
        elif self.kind == "std_ulogic":
            y += "std_ulogic_vector("
            y += str(self.width - 1) + " downto 0)"
        else:
            y += "time"

        if self.default is not None:
            if self.kind == "std_logic" or self.kind == "std_ulogic":
                if isinstance(self.default, str):
                    y += " := " + self.default
                else:
                    y += " := " + bin_literal(self.width, self.default)
            else:
                y += " := " + str(self.default)

        elif self.kind == "std_logic" or self.kind == "std_ulogic":
            y += " := " + bin_literal(self.width, 0)

        return [y]

    def declare_verilog(self):
        raise NotImplemented()

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

    uut4 = Generic(name="GENERIC_4", kind="std_logic", default=78768768, width=32)
    print(uut4.declare_vhdl()[0])

    uut5 = Generic(name="GENERIC_5", kind="std_logic", width=16)
    print(uut5.declare_vhdl()[0])

    uut6 = Generic(name="GENERIC_6", kind="std_ulogic", default=320000291, width=48)
    print(uut6.declare_vhdl()[0])

    uut7 = Generic(name="GENERIC_7", kind="std_ulogic", width=12)
    print(uut7.declare_vhdl()[0])

    uut8 = Generic(name="GENERIC_8", kind="std_ulogic", default=all_ones_binary(32), width=32)
    print(uut8.declare_vhdl()[0])
