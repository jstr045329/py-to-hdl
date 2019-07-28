def guarantee_whitespace(my_expr):
    my_expr = my_expr.replace("(", " ( ")
    my_expr = my_expr.replace(")", " ) ")
    my_expr = my_expr.replace("&&", " && ")
    my_expr = my_expr.replace("||", " || ")
    my_expr = my_expr.replace("^", " ^ ")
    my_expr = my_expr.replace("!", " ! ")
    return my_expr


def parse_expression(my_expr):
    my_expr = guarantee_whitespace(my_expr)
    y = ''
    equal_to_zero = False
    for one_tok in my_expr.split():
        if one_tok == "(":
            y += "("
        elif one_tok == ")":
            y += ")"
        elif one_tok == "!":
            equal_to_zero = True
        elif one_tok == "&&":
            y += " and "
        elif one_tok == "||":
            y += " or "
        elif one_tok == "^":
            y += " xor "
        else:
            y += one_tok
            y += " = '"
            y += "0" if equal_to_zero else "1"
            y += "'"
            equal_to_zero = False
    return y


if __name__ == "__main__":
    print(parse_expression("((x && !y)||!joe)"))
