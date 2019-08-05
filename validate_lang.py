"""Contains a tool to enforce consistent target language names across the project."""


def validate_lang(s):
    assert(s == "vhdl" or s == "verilog")


def comment_start(target_lang):
    validate_lang(target_lang)
    if target_lang == "vhdl":
        return "-- "
    else:
        return "// "
