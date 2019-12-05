from lark import Lark, InlineTransformer
from pathlib import Path

from .runtime import Symbol


class LispTransformer(InlineTransformer):
    number = float

    def start(self, *args):
        return [Symbol.BEGIN, *args]

    def name(self, *args):
        string = str(args[0])
        string = string[1:len(args[0]) - 1]
        string = string.replace(r'\n', "\n")
        string = string.replace(r'\t', "\t")
        string = string.replace("\\", "")
        return string

    def lists(self, *args):
        return list(args)

    def quote(self, *args):
        x, *y = args
        return [Symbol.QUOTE, args[0]]

    def boolean(self, *args):
        return str(args[0]) == "#t"

    def symbol(self, *args):
        return Symbol(args[0])

    def operators(self, *args):
        op = [args[1], args[0], args[2]]
        return (op)

    def let(self, *args):
        *x, y = args
        dic = []

        mylist = dic
        for i in range(0, len(x), 2):
            mylist.append([x[i], x[i+1]])

        return [Symbol.LET, dic, y]

#     def if_func(self, *args):
#         x = args
#         dic = []
#         get_if_list(dic, args)
#         return dic


# def get_if_list(list, args):
#     x = args
#     list.append([Symbol.IF, x[0], x[1]])
#     if len(x) > 2:
#         get_if_list(list[0], x[2:])


def parse(src: str):
    """
    Compila string de entrada e retorna a S-expression equivalente.
    """
    return parser.parse(src)


def _make_grammar():
    """
    Retorna uma gramática do Lark inicializada.
    """

    path = Path(__file__).parent / 'grammar.lark'
    with open(path) as fd:
        grammar = Lark(fd, parser='lalr', transformer=LispTransformer())
    return grammar


parser = _make_grammar()
