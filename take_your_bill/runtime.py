import math
import operator as op
from collections import ChainMap
from types import MappingProxyType

from .symbol import Symbol


def eval(x, bill=0, env=None):
    """
    Avalia expressão no ambiente de execução dado.
    """

    if len(x) == 0:
        return bill

    y = x.pop(0)

    # Avalia tipos atômicos
    if y == Symbol.BEGIN:
        return eval(x, bill, env)

    if env == None:
        env = standard_env


    head = y[0]

    if head == 'adiciona':  # somar
        arg = y[1]
        new_bill = bill
        if arg < 0:
            print('se tu não sabe, isso subtrai')
        else:
            new_bill = bill + arg
        return eval(x, new_bill, env)
    
    elif head == 'eu':  # somar
        arg = y[1]
        arg = arg.strip('"')
        new_bill = bill
        if arg in env:
            new_bill = bill + env[arg]
        else:
            print('não temos isso no cardápio );')
        return eval(x, new_bill, env)

    elif head == 'retira':  # subtrair
        arg = y[1]
        new_bill = bill
        if bill - arg < 0:
            print('quer pagar pra estar aqui é? não da pra retirar da conta não')
        else:
            new_bill = bill - arg
        return eval(x, new_bill, env)

    elif head == 'desejo':  # multiplicação
        arg = y[1]
        new_bill = bill
        if arg <= 0:
            print('impossivel um bacalhau assim')
        else:
            new_bill = bill * arg
        return eval(x, new_bill, env)

    elif head == 'parcela':  # divisão
        arg = y[1]
        new_bill = bill
        if arg <= 0:
            print('nao dá parcelar isso mano, so sorry')
        else:
            new_bill = bill / arg
        return eval(x, new_bill, env)

    elif head == 'da':  # porcentagem
        arg = y[1]
        new_bill = bill - (bill * arg / 100)
        return eval(x, new_bill, env)
    elif head == 'desce':  # valor do bill
        print(bill)
        return eval(x, bill, env)
    elif head == 'manda':  # cardapio completo
        for key,val in env.items():
            print (key, " => ", val, " reais")
        return eval(x, bill, env)

    elif head == 'add cardapio':  # adicionar ao cardapio
        name = y[1]
        name = name.strip('"')
        value = y[2]
        env[name] = value
        print(name, "adicionado ao cardápio, senhor")
        return eval(x, bill, env)

    elif head == 'add qtd':  # adiciona à conta algo do cardapio com quantidade definida
        value = y[1]
        name = y[2]
        name = name.strip('"')
        new_bill = bill
        if name in env:
            new_bill = bill + (value * env[name])
        else:
            print("não temos isso no cardápio );")
        return eval(x, new_bill, env)
    else:
        print(head)
        return eval(x, bill, env)
#
# Cria ambiente de execução.
#

standard_env = {
    'parmegiana' : 30,
    'fritas' : 10,
    'camarão' : 20,
    'cerveja' : 7,
    'pinga' : 20,
    'hamburger' : 20,
    'picanha' : 15
}


def env(*args, **kwargs):
    """
    Retorna um ambiente de execução que pode ser aproveitado pela função
    eval().

    Aceita um dicionário como argumento posicional opcional. Argumentos nomeados
    são salvos como atribuições de variáveis.

    Ambiente padrão
    >>> env()
    {...}

    Acrescenta algumas variáveis explicitamente
    >>> env(x=1, y=2)
    {x: 1, y: 2, ...}

    Passa um dicionário com variáveis adicionais
    >>> d = {Symbol('x'): 1, Symbol('y'): 2}
    >>> env(d)
    {x: 1, y: 2, ...}
    """

    kwargs = {Symbol(k): v for k, v in kwargs.items()}
    if len(args) > 1:
        raise TypeError('accepts zero or one positional arguments')
    elif len(args):
        if any(not isinstance(x, Symbol) for x in args[0]):
            raise ValueError('keys in a environment must be Symbols')
        args[0].update(kwargs)
        return ChainMap(args[0], global_env)
    return ChainMap(kwargs, global_env)


def _make_global_env():
    """
    Retorna dicionário fechado para escrita relacionando o nome das variáveis aos
    respectivos valores.
    """

    dic = {
        **vars(math),  # sin, cos, sqrt, pi, ...
        '+': op.add, '-': op.sub, '*': op.mul, '/': op.truediv,
        '>': op.gt, '<': op.lt, '>=': op.ge, '<=': op.le, '=': op.eq,
        'abs':     abs,
        'append':  op.add,
        'apply': lambda proc, args: proc(*args),
        'begin': lambda *x: x[-1],
        'car': lambda x: head,
        'cdr': lambda x: x[1:],
        'cons': lambda x, y: [x] + y,
        'eq?':     op.is_,
        'expt':    pow,
        'equal?':  op.eq,
        'even?': lambda x: x % 2 == 0,
        'length':  len,
        'list': lambda *x: list(x),
        'list?': lambda x: isinstance(x, list),
        'map':     map,
        'max':     max,
        'min':     min,
        'not':     op.not_,
        'null?': lambda x: x == [],
        'number?': lambda x: isinstance(x, (float, int)),
        'odd?': lambda x: x % 2 == 1,
        'print': print,
        'procedure?': callable,
        'quotient': op.floordiv,
        'round':   round,
        'symbol?': lambda x: isinstance(x, Symbol),
    }
    return MappingProxyType({Symbol(k): v for k, v in dic.items()})


global_env = _make_global_env()
