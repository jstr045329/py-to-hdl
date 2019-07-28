def basic_signal():
    return "std_ulogic_vector"


def vhd_int(lower_lim=None, upper_lim=None):
    if upper_lim is not None:
        assert lower_lim is not None
    if lower_lim is not None:
        assert upper_lim is not None
    return "integer"

