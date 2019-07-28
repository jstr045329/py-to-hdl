def basic_signal(width=1):
    assert(width >= 1)
    return "std_ulogic_vector(" + str(width-1) + " downto 0)"


def vhd_int(lower_lim=None, upper_lim=None):
    if upper_lim is not None:
        assert lower_lim is not None
    if lower_lim is not None:
        assert upper_lim is not None
    return "integer"

