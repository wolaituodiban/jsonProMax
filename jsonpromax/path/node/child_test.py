from datetime import datetime as ddt
import jsonpromax as jpm
from tqdm import trange


def test_child_no_op():
    a = {'a': {'a': '2021-01-02'}}
    node = jpm.path.Child.from_json_path('$.a')[0]
    print(node)
    b = node(a)
    assert a == {'a': {'a': '2021-01-02'}}, a
    assert b == {'a': '2021-01-02'}, b

    for _ in trange(10000000, desc='no_op'):
        node({'a': {'a': '2021-01-02'}})


def test_child_with_op():
    a = {'a': {'a': '2021-01-02'}}
    now = ddt.strptime('2021-01-03', '%Y-%m-%d')
    node = jpm.path.Child.from_json_path('$.a')[0]
    node.insert(jpm.Timestamp('a', '%Y-%m-%d', ['month', 'day']))
    print(node)
    b = node(a, now=now)
    assert b == {'a': {'a': '2021-01-02', 'a_month': 1, 'a_day': 2, 'diff_day': 1}}, b
    assert a == {'a': {'a': '2021-01-02'}}, a

    for _ in trange(1000000, desc='op outplace'):
        node({'a': {'a': '2021-01-02'}}, now=now)

    node.inplace(True)
    b = node(a, now=now)
    assert b == {'a': {'a': '2021-01-02', 'a_month': 1, 'a_day': 2, 'diff_day': 1}}, b
    assert a == b, a
    for _ in trange(1000000, desc='op inplace'):
        node({'a': {'a': '2021-01-02'}}, now=now)


if __name__ == '__main__':
    test_child_no_op()
    test_child_with_op()
