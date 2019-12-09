from take_your_bill import var, env, Symbol, parse, eval, global_env

run = lambda src, env=None: eval(parse(src), env)
x, y, a, b, c, f, g, h, op = map(Symbol, 'x y a b c f g h op'.split())


class TestLispGrammar:
    def test_numbers(self):
        assert parse('42') == 42
        assert parse('3.14') == 3.14
        assert parse('-3.14') == -3.14

    def test_atomic(self):
        assert parse('#t') is True
        assert parse('#f') is False
        assert parse('x') == x
        assert parse('-') == Symbol('-')
        assert parse('expt') == Symbol('expt')
        assert 

class TestEnvCreation:
    def test_env_creation(self):
        assert env() == global_env
        assert set(env({var.x: 42})).issuperset(set(global_env))
        assert env({var.x: 42})[var.x] == 42
        assert env(x=42)[var.x] == 42


class TestRuntime:
    def test_eval_simple(self):
        assert run('adiciona ao pedido 10 desce a conta chefia') == 10
        assert run('desejo um bacalhau de 5 desce a conta chefia') == 0
        assert run('desejo uma tilapia 2 desce a conta chefia') == 7.38905609893065
        assert run('adiciona ao pedido 4 desejo uma batata frita desce a conta chefia') == 2
        assert run('adiciona ao pedido 10 campeão, da um desconto ai de 10 desce a conta chefia') == 1

    def test_eval_if_simple(self):
        assert run('parcela ai em 0') == 'nao dá mano, so sorry'
        assert run('parcela ai em -13') == 'ai tu quer né'

    def test_eval_if_nested(self):
        assert run('retira da conta -1') == 'quer pagar pra estar aqui é?'
  