"""Contains tools to generate literals in VHDL"""


def bin_literal(num_digits, n=1):
    """Like hex_literal(), but with single quotes."""
    y = bin(n)
    y = y[2:]
    if len(y) < num_digits:
        num_zeros = num_digits - len(y)
        zero_str = "0" * num_zeros
        y = zero_str + y
    # todo: insert underscores
    return 'B"' + y + '"'


def hex_literal(num_digits, n=1):
    """Like bin_literal(), but with double quotes."""
    y = hex(n)
    y = y[2:]
    if len(y) < num_digits:
        num_zeros = num_digits - len(y)
        zero_str = "0" * num_zeros
        y = zero_str + y
    # todo: insert underscores
    return 'X"' + y + '"'


def all_ones_binary(num_digits):
    return 'B"' + ("1" * num_digits) + '"'


def all_ones_hex(num_digits):
    return 'X"' + ("F" * num_digits) + '"'


if __name__ == "__main__":
    print(bin_literal(64, 2934872938))
    print(hex_literal(32, 93920394820394802934802934802394))
