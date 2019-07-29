def common_synth_datatype():
    return "std_ulogic_vector"


def basic_signal(width=1):
    assert(width >= 1)
    return common_synth_datatype() + "(" + str(width-1) + " downto 0)"


def vhd_int(lower_lim=None, upper_lim=None):
    if upper_lim is not None:
        assert lower_lim is not None
    if lower_lim is not None:
        assert upper_lim is not None
    return "integer"

