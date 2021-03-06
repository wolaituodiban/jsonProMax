from inspect import isfunction
from itertools import combinations

import pandas as pd
from .operator import Operator


def get_name(f):
    if isinstance(f, str):
        return f
    elif isfunction(f):
        return f.__name__
    else:
        return f.__class__.__name__


class ListFeature(Operator):
    def __init__(self, time_key=None, seconds=None, minutes=None, hours=None, days=None, funcs=None, binary_funcs=None,
                 corr=False, first_last=True):
        super().__init__(inplace=False)
        self.time_key = time_key
        seconds = seconds or []
        minutes = minutes or []
        hours = hours or []
        days = days or []
        self.seconds = seconds + [x * 60 for x in minutes] + [x * 3600 for x in hours] + [x * 86400 for x in days]
        funcs = funcs or []
        self.funcs = {get_name(f): f for f in funcs}
        binary_funcs = binary_funcs or {}
        self.binary_funcs = {get_name(f): f for f in binary_funcs}
        self.corr = corr
        self.first_last = first_last

    def _time_key(self, time):
        for i, second in enumerate(self.seconds):
            if time < second:
                if i == 0:
                    return '0s~{}s'.format(int(second))
                else:
                    return '{}s~{}s'.format(int(self.seconds[i - 1]), int(second))

    def _call_df(self, df):
        outputs = {}
        if self.first_last:
            outputs.update({'first({})'.format(k): v for k, v in df.iloc[0].items()})
            outputs.update({'last({})'.format(k): v for k, v in df.iloc[-1].items()})
        if self.corr and df.shape[1] > 1:
            corr = df.corr()
            for c1, c2 in combinations(df, 2):
                outputs['corr({c1}, {c2})'.format(c1=c1, c2=c2)] = corr.loc[c1, c2]
        if len(self.funcs) > 0:
            for f_name, f in self.funcs.items():
                outputs.update(
                    {'{f_name}({k})'.format(f_name=f_name, k=k): v for k, v in df.apply(f).items()}
                )
        if len(self.binary_funcs) > 0:
            for k, f in self.binary_funcs.items():
                for c1, c2 in combinations(df, 2):
                    outputs['{k}({c1}, {c2})'.format(k=k, c1=c1, c2=c2)] = f(df[c1], df[c2])
                    c1, c2 = c2, c1
                    outputs['{k}({c1}, {c2})'.format(k=k, c1=c1, c2=c2)] = f(df[c1], df[c2])
        return outputs

    def __call__(self, obj, **kwargs):
        df = pd.DataFrame(obj)
        if df.shape[0] == 0:
            return dict()
        outputs = self._call_df(df)
        outputs['length'] = df.shape[0]
        if self.time_key is not None and self.time_key in df and len(self.seconds) > 0:
            for s, g in df.groupby(df[self.time_key].apply(self._time_key)):
                g.columns = ['{s}({c})'.format(s=s, c=c) for c in g.columns]
                outputs.update(self._call_df(g))
                outputs['length({s})'.format(s=s)] = g.shape[0]
        return {k: float(v) for k, v in outputs.items()}

#
# class ListFeatureLite(Operator):
#     np.corrcoef()
#     pass


class CountListItem(Operator):
    def __init__(self, key, inplace=False):
        super().__init__(inplace=inplace)
        self.key = key

    def _call(self, obj, **kwargs):
        if self.key not in obj:
            return obj
        obj = dict(obj)
        count = {}
        for v in obj[self.key]:
            if v in count:
                count[v] += 1
            else:
                count[v] = 1
        for k, v in count.items():
            obj['count({}.{})'.format(self.key, k)] = v
        return obj

    def _call_inplace(self, obj, **kwargs):
        if self.key not in obj:
            return obj
        count = dict()
        for v in obj[self.key]:
            if v in count:
                count[v] += 1
            else:
                count[v] = 1
        for k, v in count.items():
            obj['count({}.{})'.format(self.key, k)] = v
        return obj


class OneHot(Operator):
    def __init__(self, key, inplace=False):
        super().__init__(inplace=inplace)
        self.key = key

    def _call(self, obj, **kwargs):
        if self.key not in obj:
            return obj
        obj = dict(obj)
        obj['{}={}'.format(self.key, obj[self.key])] = 1
        return obj

    def _call_inplace(self, obj, **kwargs):
        if self.key not in obj:
            return obj
        obj['{}={}'.format(self.key, obj[self.key])] = 1
        return obj
