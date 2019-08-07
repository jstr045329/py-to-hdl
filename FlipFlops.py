from BaseTools import BasicDevice
from CentralNameGen import CentralNameGen
from DataTypes import basic_signal
from IO import Input
from IO import Output
from Signal import Signal
from WhiteSpaceTools import tab
from WhiteSpaceTools import eol

from Entity import Entity


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
        # todo: add capability to render signals as bit
        # todo: add capability to leave resets out
        # todo: add capability to assign ff's to 0 by default
        # todo: add fast mode, which does all 3

def make_one_input_name(kind, n):
    if kind == "r":
        stub = "rst_"
    elif kind == "s":
        stub = "set_"
    elif kind == "t":
        stub = "tog_"
    return stub + ("%04d" % n)

class CustomFFModule(Entity):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        from copy import deepcopy
        new_kwargs = deepcopy(kwargs)
        del (new_kwargs["name"])
        if "expression" in new_kwargs:
            del(new_kwargs["expression"])
        if "central_name_gen" in new_kwargs:
            new_kwargs["central_name_gen"] = kwargs["central_name_gen"]
        self.taps = []
        self.add_input(Input(name="clk",
                             width=1,
                             expression="",
                             **new_kwargs))

        self.input_list = kwargs["input_list"]
        num_resets = 0
        num_sets = 0
        num_toggles = 0
        self.input_name_list = []
        for one_char in kwargs["input_list"]:
            if one_char.lower() == "r":
                one_name = "rst_" + ("%04d" % num_resets)
                one_sig = Input(name=one_name, width=1, expression="", **new_kwargs)
                self.add_input(one_sig)
                self.add_device(one_sig)
                num_resets += 1
                self.input_name_list.append(one_name)
            if one_char.lower() == "s":
                one_name = "set_" + ("%04d" % num_sets)
                one_sig = Input(name=one_name, width=1, expression="", **new_kwargs)
                self.add_input(one_sig)
                self.add_device(one_sig)
                num_sets += 1
                self.input_name_list.append(one_name)
            if one_char.lower() == "t":
                one_name = "tog_" + ("%04d" % num_toggles)
                one_sig = Input(name=one_name, width=1, expression="", **new_kwargs)
                self.add_input(one_sig)
                self.add_device(one_sig)
                num_toggles += 1
                self.input_name_list.append(one_name)

        out_sig = Signal(name="q_sig", width=1, expression="", **new_kwargs)
        self.signal_list.append(out_sig)
        self.add_output(Output(name="q", width=1, expression="", **new_kwargs))

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
        y.append("process(clk)")
        y.append("begin")
        y.append(tab(1) + "if rising_edge(clk) then")
        y.append(tab(2) + "if rst_global = '1' then")
        y.append(tab(3) + "q0 <= (others => '0');")
        for one_input in self.input_name_list:
            y.append(tab(2) + "elsif " + one_input + " = '1' then")
            if "set" in one_input:
                y.append(tab(3) + "q0(0) <= '1';")
            elif "rst" in one_input:
                y.append(tab(3) + "q0(0) <= '0';")
            elif "tog" in one_input:
                y.append(tab(3) + "q0(0) <= not q0(0);")
        y.append(tab(2) + "end if; ")
        y.append(tab(1) + "end if; ")
        y.append("end process;")
        y.append("q <= q0;")

        y.append("end " + self.name + "_arch;")
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


def test_basic_delay():
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


def test_delay_module():
    cng = CentralNameGen()
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


def test_custom_ff_module():
    cng = CentralNameGen()
    uut = CustomFFModule(name="custom_ff_mod",
                         clk="clk",
                         rst="rst",
                         central_name_gen=cng,
                         input_list="rssrrtt")
    for i in uut.render_vhdl():
        print(i)


if __name__ == "__main__":
    test_basic_delay()
    test_delay_module()
    test_custom_ff_module()




