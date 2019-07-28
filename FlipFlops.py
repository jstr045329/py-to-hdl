from BaseTools import BasicDevice
from WhiteSpaceTools import tab


class FlipFlop(BasicDevice):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


def reset_assignment(name, num):
    return name + "_" + ("%06d" % num) + " <= (others => '0');"


def delay_assignment(name, num):
    one_str = name + "_" + ("%06d" % (num+1))
    one_str += " <= "
    one_str += name + "_" + ("%06d" % num)
    one_str += ";"
    return one_str


class BasicDelay(FlipFlop):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if "num_delays" in kwargs:
            self.num_delays = kwargs["num_delays"]
        else:
            self.num_delays = 1
        self.clk = kwargs["clk"]
        self.rst = kwargs["rst"]

    def render_vhdl(self):
        y = []
        sens_list = "(" + self.clk + ", " + self.rst + ")"
        y.append("process" + sens_list)
        y.append("begin")
        y.append(tab() + "if " + self.rst + " = '1' then")
        for i in range(self.num_delays+1):
            y.append(tab(n=2) + reset_assignment(self.name, i))
        y.append(tab() + "elsif rising_edge(" + self.clk + ") then")
        for i in range(self.num_delays):
            y.append(tab(n=2) + delay_assignment(self.name, i))
        y.append(tab() + "end if;")
        y.append("end process;")
        return y


if __name__ == "__main__":
    uut = BasicDelay(name="myDelay", num_delays=8, clk="clk", rst="rst")
    for i in uut.render_vhdl():
        print(i)
