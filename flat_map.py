"""Contains a function to append each list in a list of lists, apply some function to each element, and return a flat
list."""


def flat_map(list_of_lists, some_function):
    y = []
    for i in list_of_lists:
        y.extend(some_function(i))
    return y
