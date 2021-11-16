import jsonpromax as jpm


def test_mean():
    op = jpm.Mean()
    result = op([0, 1])
    assert result == 0.5, result
    result = op({'a': 0, 'b': 1})
    assert result == 0.5, result


if __name__ == "__main__":
    test_mean()
