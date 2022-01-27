from datetime import datetime as ddt
from multiprocessing import Pool
from typing import Iterable

import pandas as pd


from .path import JsonPathTree

try:
    from tqdm import tqdm
except ImportError:
    def tqdm(x, *args, **kwargs):
        return x


class FeatureDerivation(JsonPathTree):
    def __init__(self, json_col, time_col, time_format, processors, tokenizer=None, **kwargs):
        super().__init__(processors=processors, **kwargs)
        self.json_col = json_col
        self.time_col = time_col
        self.time_format = time_format
        self.tokenizer = tokenizer

    def derivate(self, df: pd.DataFrame, disable=True):
        def strptime(s):
            if pd.notna(s):
                return ddt.strptime(s, self.time_format)

        iterable = (
            self(row[self.json_col], now=strptime(row[self.time_col]), tokenizer=self.tokenizer)
            for _, row in df.iterrows()
        )
        features = pd.DataFrame(tqdm(iterable, disable=disable))
        df = df.drop(columns='data').copy()
        df[features.columns] = features.values
        return df

    def to_csv(self, dfs: Iterable[pd.DataFrame], dst: str, pre_nrows=1000, processes=None, disable=True):
        """

        Args:
            dfs:
            dst:
            pre_nrows: 由于每一个样本衍生出的特征可能不一样，需要感觉前n个样本确定最终文件的列数
            processes: 多进程个数
            disable:

        Returns:

        """
        with Pool(processes=processes) as pool, open(dst, 'w') as file:
            buffer = pd.DataFrame()
            columns = None
            for df in tqdm(pool.imap_unordered(self.derivate, dfs), disable=disable):
                if columns is None:
                    # 首先根据前chunksize个判断特征数量
                    buffer = pd.concat([buffer, df])
                    if buffer.shape[0] > pre_nrows:
                        columns = df.columns
                        buffer.to_csv(file, index=False)
                        buffer = None
                else:
                    for col in columns:
                        if col not in df:
                            df[col] = None
                    df = df[columns]
                    df.to_csv(file, header=False, index=False)
            if buffer is not None:
                buffer.to_csv(file, index=False)
