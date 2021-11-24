import jsonpromax as jpm


def test_rename():
    op = jpm.Rename('a', 'b')
    a = {'a': 1}
    b = op(a)
    assert a == {'a': 1}, a
    assert b == {'b': 1}, b
    op.inplace(inplace=True)
    c = op(a)
    assert c == {'b': 1} == a, (a, c)


if __name__ == '__main__':
    test_rename()
