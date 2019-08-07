"""Contains the superclass from which all other device classes are derived."""
from validate_lang import validate_lang


class BasicDevice:
    def __init__(self, name, comment="", parent=None, **kwargs):
        if "target_lang" in kwargs:
            self.target_lang = kwargs["target_lang"]
        elif parent is not None:
            self.target_lang = parent.target_lang
        else:
            self.target_lang = "vhdl"
        validate_lang(self.target_lang)
        self.children = []
        self.in_list = []
        self.out_list = []
        self.signal_list = []
        self.comment = []
        self.comment.extend(comment)
        self.name = name
        self.parent = parent
        if parent is None:
            self.my_level = 0
        else:
            self.my_level = parent.my_level + 1
        self.declared_ins = []
        self.declared_outs = []
        self.declared_signals = []
        self.declared_components = []
        self.central_name_gen = kwargs["central_name_gen"]
        self.use_bit_when_possible = False          # todo: use this to render bit(vector) rather than std_logic(vector).
        self.default_resolved = False
        self.initialize_signals_to_zero = False     # todo: use this to assign default values to signals

    def get_default_datatype(self, width):
        # todo: replace the static .py file with this
        assert(width >= 1)
        if self.use_bit_when_possible:
            return "bit_vector(" + str(width-1) + " downto 0)"
        if self.default_resolved:
            return "std_logic_vector(" + str(width-1) + " downto 0)"
        return "std_ulogic_vector(" + str(width-1) + " downto 0)"

    def get_datatype_root(self):
        x = self.get_default_datatype(width=1)
        stop_idx = x.find("(")
        return x[:stop_idx]

    def add_device(self, child):
        self.children.append(child)

    def add_input(self, x):
        self.in_list.append(x)

    def add_output(self, x):
        self.out_list.append(x)

    def render(self):
        if self.target_lang == "vhdl":
            return self.render_vhdl()
        else:
            return self.render_verilog()

    def input_is_declared(self, nm):
        return nm in self.declared_ins

    def output_is_declared(self, nm):
        return nm in self.declared_outs

    def signal_is_declared(self, nm):
        return nm in self.declared_signals

    def component_is_declared(self, nm):
        return nm in self.declared_components

    def declare_vhdl(self):
        raise NotImplemented()

    def declare_verilog(self):
        raise NotImplemented()

    def logic_vhdl(self):
        raise NotImplemented()

    def logic_verilog(self):
        raise NotImplemented()

    def render_vhdl(self):
        raise NotImplemented()

    def render_verilog(self):
        raise NotImplemented()





