from lark import Lark, InlineTransformer
from pathlib import Path

from re import split
from .runtime import Symbol


class LispTransformer(InlineTransformer):
    number = float

    def start(self, *args):
        return [Symbol.BEGIN, *args]

    def speak(self, *args):
        string = str(args[0])
        string = string[1:len(args[0]) - 1]
        string = string.replace(r'\n', "\n")
        string = string.replace(r'\t', "\t")
        string = string.replace("\\", "")
        return [string]

    def operators(self, *args):
        head = args[0]
        if head.type == 'INITIAL_PARAMETER':
            head = split(r'\s+', str(head))
            if head[0] == 'adiciona':
                return ['add cardapio' ,str(args[1]), float(args[2])]
            return ['add qtd' , int(args[1]), str(args[2])]
        if head.type == 'SIGLE_OPERATOR':
            head = split(r'\s+', str(head))
            return [head[0]]
        if head.type == 'OPERATORS':
            head = split(r'\s+', str(head))
            return [head[0], args[1]]
            
        return head.type

    def single_operator(self, *args):
        return [str(args[0])]

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
