from BaseTools import BasicDevice
from WhiteSpaceTools import tab
from WhiteSpaceTools import eol
from DataTypes import basic_signal
from Entity import Entity
from IO import Input
from IO import Output


class FlipFlop(BasicDevice):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


def one_tap_name(n):
    return "tap_" + ("%06d" % n)


def one_signal_name(name, num):
    return name + "_" + ("%06d" % num)


def declare_1_signal(name, num, width):
    return "signal " + one_signal_name(name, num) + " : " + basic_signal(width=width) + ";"


def reset_assignment(name, num):
    return one_signal_name(name, num) + " <= (others => '0');"


def delay_assignment(name, num):
    one_str = one_signal_name(name, num+1)
    one_str += " <= "
    one_str += one_signal_name(name, num)
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
        self.width = kwargs["width"]

    def declare_vhdl(self):
        y = []
        for i in range(0, self.num_delays+1):
            y.append(declare_1_signal(self.name, i, self.width))
        return y

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


class DelayModule(Entity):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        from copy import deepcopy
        new_kwargs = deepcopy(kwargs)
        del(new_kwargs["name"])
        del(new_kwargs["width"])
        if "expression" in new_kwargs:
            del(new_kwargs["expression"])
        if "central_name_gen" in new_kwargs:
            new_kwargs["central_name_gen"] = kwargs["central_name_gen"]
        self.children.append(BasicDelay(**kwargs))
        self.taps = []
        self.add_input(Input(name="clk",
                             width=1,
                             expression="",
                             **new_kwargs))
        self.add_input(Input(name="rst", width=1, expression="", **new_kwargs))
        self.add_input(Input(name="d_in", width=self.children[0].width, expression="", **new_kwargs))
        self.add_output(Output(name="d_out", width=self.children[0].width, expression="", **new_kwargs))
        # self.add_output()

    def add_tap(self, n):
        if isinstance(n, list):
            for one_tap in n:
                self.taps.append(one_tap)
                this_name = "tap_" + ("%06d"%one_tap)
                self.add_output(Output(name=this_name,
                                       width=self.children[0].width,
                                       expression="",
                                       central_name_gen=self.central_name_gen))
        else:
            assert(isinstance(n, int))
            self.taps.append(n)
            this_name = "tap_" + ("%06d" % n)
            self.add_output(Output(name=this_name,
                                   width=self.children[0].width,
                                   expression="",
                                   central_name_gen=self.central_name_gen))

    def render_vhdl(self):
        y = []
        y.append("library IEEE;")
        y.append("use IEEE.STD_LOGIC_1164.all;")
        y.append(eol())
        y.append("entity " + self.name + " is")
        y.append("port(")
        for i in range(len(self.in_list)):
            one_thing = self.in_list[i]
            one_str = tab() + one_thing.declare_vhdl()[0]
            y.append(one_str)
        for i in range(len(self.out_list)):
            one_thing = self.out_list[i]
            one_str = tab() + one_thing.declare_vhdl()[0]
            if i == len(self.out_list) - 1:
                one_str = one_str[:-1] + ");"
            y.append(one_str)
        y.append("end " + self.name + ";")
        y.append(eol())
        y.append("architecture " + self.name + "_arch of " + self.name + " is")
        for i in self.children[0].declare_vhdl():
            y.append(tab() + i)
        y.append("begin")
        for i in self.children[0].render_vhdl():
            y.append(tab() + i)
        y.append(tab() + one_signal_name(self.name, 0) + " <= d_in;")
        for one_tap in self.taps:
            y.append(tab() + one_tap_name(one_tap) + " <= " + one_signal_name(self.name, one_tap) + ";")
        y.append(tab() + "d_out <= " + one_signal_name(self.name, self.children[0].num_delays) + ";")
        y.append("end " + self.name + "_arch;")
        return y


if __name__ == "__main__":
    from CentralNameGen import CentralNameGen
    cng = CentralNameGen()
    uut = BasicDelay(name="myDelay",
                     num_delays=8,
                     clk="clk",
                     rst="rst",
                     width=4,
                     central_name_gen=cng)

    for i in uut.declare_vhdl():
        print(i)
    for i in uut.render_vhdl():
        print(i)
    print(eol(4))
    uut2 = DelayModule(name="delayModule",
                       num_delays=32,
                       clk="clk",
                       rst="rst",
                       width=16,
                       central_name_gen=cng)
    uut2.add_tap(4)
    uut2.add_tap([17, 26, 31])
    for i in uut2.render_vhdl():
        print(i)

# TODO Fix all unit tests




