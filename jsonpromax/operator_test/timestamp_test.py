from datetime import datetime as ddt
import jsonpromax as jpm
from tqdm import trange


def test_timestamp():
    op = jpm.Timestamp('a', '%Y-%m-%d', ['month', 'day'])
    print(op)
    now = ddt.strptime('2021-01-03', '%Y-%m-%d')
    a = {'a': '2021-01-02'}
    b = op(a, now=now)
    assert b == {'a': '2021-01-02', 'a_month': 1, 'a_day': 2, 'diff_day': 1}, b
    assert a == {'a': '2021-01-02'}, a

    for _ in trange(1000000, desc='1 outplace'):
        op({'a': '2021-01-02'})

    op.inplace(True)
    c = op(a, now=now)
    assert a == c == {'a': '2021-01-02', 'a_month': 1, 'a_day': 2, 'diff_day': 1}, (a, c)

    for _ in trange(1000000, desc='1 inplace '):
        op({'a': '2021-01-02'})


def test_timestamp2():
    op = jpm.Timestamp2('%Y-%m-%d', ['month', 'day'], second=False)
    print(op)
    now = ddt.strptime('2021-01-03', '%Y-%m-%d')
    a = '2021-01-02'
    b = op(a, now=now)
    assert b == {'month': 1, 'day': 2, 'diff_day': 1}, b

    for _ in trange(1000000, desc='2 outplace'):
        op(a)


def test_timestamp3():
    op = jpm.Timestamp3('a', '%Y-%m-%d', ['month', 'day'])
    print(op)
    now = ddt.strptime('2021-01-03', '%Y-%m-%d')
    a = {'a': '2021-01-02'}
    b = op(a, now=now)
    assert b == {'a': '2021-01-02', 'month': 1, 'day': 2, 'diff_second': 86400.0}, b
    assert a == {'a': '2021-01-02'}, a

    for _ in trange(1000000, desc='3 outplace'):
        op({'a': '2021-01-02'})
    #
    op.inplace(True)
    c = op(a, now=now)
    assert a == c == {'a': '2021-01-02', 'month': 1, 'day': 2, 'diff_second': 86400.0}, (a, c)

    for _ in trange(1000000, desc='3 inplace '):
        op({'a': '2021-01-02'})


def test_timestamp4():
    op = jpm.Timestamp4('a', '%Y-%m-%d', ['month', 'day'])
    print(op)
    now = ddt.strptime('2021-01-03', '%Y-%m-%d')
    a = {'a': '2021-01-02'}
    b = op(a, now=now)
    assert b == {'a': '2021-01-02', 'a_month': 1, 'a_day': 2, 'a_diff_day': 1}, b
    assert a == {'a': '2021-01-02'}, a

    for _ in trange(1000000, desc='4 outplace'):
        op({'a': '2021-01-02'})

    op.inplace(True)
    c = op(a, now=now)
    assert a == c == {'a': '2021-01-02', 'a_month': 1, 'a_day': 2, 'a_diff_day': 1}, (a, c)

    for _ in trange(1000000, desc='4 inplace '):
        op({'a': '2021-01-02'})


if __name__ == '__main__':
    test_timestamp()
    test_timestamp2()
    test_timestamp3()
    test_timestamp4()
