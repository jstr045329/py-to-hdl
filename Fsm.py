from BaseTools import BasicDevice


def validate_implementation_mode(mode):
    assert(mode == "integer" or
           mode == "one_hot" or
           mode == "redundant_3" or
           mode == "redundant_5")


def parse_condition(condition: str):
    output_condition = ''
    input_list = []
    output_list = []
    condition = condition.replace("(", " ( ")
    condition = condition.replace(")", " ) ")
    tok_list = condition.split()
    # ACTION: Finish parsing condition
    return output_condition, input_list, output_list


class FiniteStateMachine(BasicDevice):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.state_list = []
        self.mode = "integer"
        self.implementation_mode_set = False
        self.transition_list = []
        self.make_own_entity = False

    def enable_own_entity(self):
        """Call this to spawn the FSM as its own entity"""
        self.make_own_entity = True

    def set_implementation_mode(self, mode):
        """This function is optional, but you can only call it once."""
        assert(not self.implementation_mode_set)
        validate_implementation_mode(mode)
        self.mode = mode
        self.implementation_mode_set = True

    def add_state(self, state_name, **kwargs):
        assert(state_name not in self.state_list)
        self.state_list.append(state_name)

    def add_transition(self, from_state, to_state, condition, **kwargs):
        assert(from_state in self.state_list)
        assert(to_state in self.state_list)
        one_condition, in_list, out_list = parse_condition(condition)
        for one_input in in_list:
            if one_input not in self.in_list:
                self.add_input(one_input)
        for one_output in out_list:
            if one_output not in self.out_list:
                self.add_output(one_output)
        self.transition_list.append(one_condition)

    def render_vhdl(self):
        pass

    def render_verilog(self):
        pass







