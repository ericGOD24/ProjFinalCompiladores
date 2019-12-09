import math
import operator as op
from collections import ChainMap
from types import MappingProxyType

from .symbol import Symbol


def eval(x, env=0):
    """
    Avalia expressão no ambiente de execução dado.
    """

    if len(x) == 0:
        return env

    y = x.pop(0)

    # Avalia tipos atômicos
    if y == Symbol.BEGIN:
        return eval(x, env)

    head = y[0]

    if head == 'adiciona ao pedido':  # somar
        arg = y[1]
        new_env = env + arg
        return eval(x, new_env)

    elif head == 'retira da conta':  # subtrair
        arg = y[1]
        new_env = env
        if env - arg < 0:
            print('quer pagar pra estar aqui é? não da pra retirar da conta não')
        else:
            new_env = env - arg
        return eval(x, new_env)

    elif head == 'desejo um bacalhau de':  # multiplicação
        arg = y[1]
        new_env = env
        if arg <= 0:
            print('impossivel um bacalhau assim')
        else:
            new_env = env * arg
        return eval(x, new_env)

    elif head == 'parcela ai em':  # divisão
        arg = y[1]
        new_env = env
        if arg <= 0:
            print('nao dá parcelar isso mano, so sorry')
        else:
            new_env = env / arg
        return eval(x, new_env)

    elif head == 'desejo uma tilapia':  # exponencial
        new_env = math.exp(env)
        return eval(x, new_env)

    elif head == 'desejo uma batata frita':  # raiz quadrada
        new_env = math.sqrt(env)
        return eval(x, new_env)

    elif head == 'campeão, da um desconto ai de':  # porcentagem
        new_env = env * arg / 100
        return eval(x, new_env)
    elif head == 'desce a conta chefia':  # valor do env
        print(env)
        return eval(x, env)
    else:
        print(head)
        return eval(x, env)
#
# Cria ambiente de execução.
#


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
