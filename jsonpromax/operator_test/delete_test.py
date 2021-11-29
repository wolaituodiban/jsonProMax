import jsonpromax as jpm
from tqdm import trange


def test_delete():
    a = {'a': 1, 'b': 2}
    op = jpm.Delete({'b'}, inplace=False)
    b = op(a)
    assert a == {'a': 1, 'b': 2}, a
    assert b == {'a': 1}, b

    op.inplace(True)
    b = op(a)
    assert a == b == {'a': 1}, (a, b)


def test_speed():
    rounds = int(1e7)
    op = jpm.Delete({'b'}, inplace=False)
    for _ in trange(rounds, desc='not inplace'):
        op({'a': 1, 'b': 2})

    op = jpm.Delete({'b'}, inplace=True)
    for _ in trange(rounds, desc='inplace'):
        op({'a': 1, 'b': 2})


if __name__ == '__main__':
    test_delete()
    test_speed()
