import jsonpromax as jpm
import numpy as np
import pandas as pd


def test_feat_deriv():
    data = [{'a': 1, 'b': 2}] * 10
    data = pd.DataFrame({'data': data})
    data['time'] = np.nan

    processor = jpm.FeatureDerivation(
        json_col='data',
        time_col='time',
        time_format=None,
        processors=[
            ('$', jpm.ListFeature(funcs=['mean']))
        ]
    )
    df = processor.derivate(data, disable=False)
    print(df)
    processor.to_csv([data], 'test.csv', disable=False)
    df2 = pd.read_csv('test.csv')
    assert df2.shape == (10, 3)
    processor.to_csv([data], 'test.csv', pre_nrows=1, disable=False)
    df3 = pd.read_csv('test.csv')
    assert df3.shape == (10, 3)


if __name__ == '__main__':
    test_feat_deriv()
