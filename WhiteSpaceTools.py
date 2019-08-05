import os


def eol(n=1):
    return os.linesep * n


def whitespace(n):
    return " " * n


def tab(n=1, width=4):
    return " " * width * n
