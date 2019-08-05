from BaseTools import BasicDevice
from Signal import Signal
from flat_map import flat_map
from Generic import Generic
from LiteralTools import all_ones_binary
from LiteralTools import bin_literal
from WhiteSpaceTools import tab


def rst_name(nm):
    return nm + "_reset_val"


def init_name(nm):
    return nm + "_init_val"


def rollover_name(nm):
    return nm + "_rollover_val"


def delta_name(nm):
    return nm + "_delta"


class Counter(BasicDevice):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.width = kwargs["width"]
        self.rollover_value = kwargs["rollover_thresh"]
        assert(2 ** self.width >= self.rollover_value)

        if "reset_val" in kwargs:
            default_reset = kwargs["reset_val"]
        else:
            default_reset = 0

        if "init_val" in kwargs:
            default_init = kwargs["init_val"]
        else:
            default_init = 0

        if "rollover_thresh" in kwargs:
            default_rollover = kwargs["rollover_thresh"]
        else:
            default_rollover = all_ones_binary(self.width)

        if "direction" in kwargs:
            self.direction = kwargs["direction"]
            assert(self.direction == "up" or self.direction == "down")
        else:
            self.direction = "up"

        if "use_clock_en" in kwargs:
            self.use_clock_en = kwargs["use_clock_en"]
            assert(isinstance(self.use_clock_en, bool))
        else:
            self.use_clock_en = True

        if "delta" in kwargs:
            default_delta = kwargs["delta"]
            assert(default_delta >= 1)
            assert(2**self.width > default_delta)
        else:
            default_delta = 1

        self.clk = kwargs["clk"]
        self.rst = kwargs["rst"]
        self.children.append(kwargs["clk"])
        self.children.append(kwargs["rst"])

        # Choose the value the counter goes to when device is reset:
        reset_val = Generic(name=rst_name(self.name),
                            width=kwargs["width"],
                            kind="std_ulogic",
                            default=default_reset,
                            central_name_gen=self.central_name_gen)

        # Choose the value the counter goes to after it rolls over:
        init_val = Generic(name=init_name(self.name),
                           width=kwargs["width"],
                           kind="std_ulogic",
                           default=default_init,
                           central_name_gen=self.central_name_gen)

        rollover_threshold = Generic(name=rollover_name(self.name),
                                     width=kwargs["width"],
                                     target_lang="vhdl",
                                     kind="std_ulogic",
                                     default=default_rollover,
                                     central_name_gen=self.central_name_gen)

        delta_obj = Generic(name=delta_name(self.name),
                            width=kwargs["width"],
                            target_lang="vhdl",
                            kind="std_ulogic",
                            default=default_delta,
                            central_name_gen=self.central_name_gen)

        count_sig = Signal(name=self.name+"_counter",
                           width=kwargs["width"],
                           target_lang="vhdl",
                           expression="",
                           central_name_gen=self.central_name_gen)

        self.children.append(reset_val)
        self.children.append(init_val)
        self.children.append(rollover_threshold)
        self.children.append(count_sig)
        self.children.append(delta_obj)
        self.reset_val = reset_val
        self.init_val = init_val
        self.rollover_threshold = rollover_threshold
        self.count_sig = count_sig
        self.delta = delta_obj

    def declare_vhdl(self):
        y = []
        for i in self.children:
            y.extend(i.declare_vhdl())
        return y

    def render_vhdl(self):
        y = []
        sens_list = "(" + self.clk.name + ", " + self.rst.name + ")"
        y.append("process" + sens_list)
        y.append("begin")
        y.append(tab() + "if " + self.rst.name + " = '1' then")
        y.append(tab(n=2) + self.count_sig.name + " <= " + self.reset_val.name + ";") # use generic here
        y.append(tab() + "elsif rising_edge(" + self.clk.name + ") then")

        y.append(tab(n=2) + "if " + self.count_sig.name + " >= " + self.rollover_threshold.name + " then")
        y.append(tab(n=3) + self.count_sig.name + " <= " + self.init_val.name + ";")
        y.append(tab(n=2) + "else")
        y.append(tab(n=3) + self.count_sig.name + " <= " + self.count_sig.name + " + " +  self.delta.name + ";")
        y.append(tab(n=2) + "end if;")
        y.append(tab() + "end if;")
        y.append("end process;")
        return y


if __name__ == "__main__":
    from CentralNameGen import CentralNameGen
    cng = CentralNameGen()
    clk = Signal(width=1, target_lang="vhdl", name="clk", expression=None, central_name_gen=cng)
    rst = Signal(width=1, target_lang="vhdl", name="rst", expression=None, central_name_gen=cng)
    uut = Counter(name="uut",
                  width=32,
                  clk=clk,
                  rst=rst,
                  init_val=32,
                  reset_val=64,
                  rollover_thresh=255,
                  delta=7,
                  central_name_gen=cng)
    for i in uut.declare_vhdl():
        print(i)
    print("\n")
    for i in uut.render_vhdl():
        print(i)

# todo: Think about what a better factoring of methods would be.
#       The same 2 functions for every class is not working.
#       Maybe entities need 1 set of methods, and everything else
#       needs a different set of methods.
# todo: Make declare_vhdl() return a tuple, (generics, ports, signals)
# todo: Make a class that spawns a new entity

# Write a list of every VHDL pattern I want to use, and look at
# what needs to get passed into what.

# Think about what classes I should write
# For example, should I write a class for process?
# Write a full list of all the

# Research how to attract volunteers


