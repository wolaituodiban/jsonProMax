import os
import shutil
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

    def to_csv(self, dfs: Iterable[pd.DataFrame], dst: str, processes=None, disable=False, dropna=0.99):
        """

        Args:
            dfs:
            dst:
            processes: 多进程个数
            disable:
            dropna: 删除缺失率大于这个值的特征
        Returns:

        """
        origin_columns = None  # 记录排在最前的几个原始字段的位置
        with Pool(processes=processes) as pool, tqdm(disable=disable, desc='stage 1') as bar:
            dir_path = dst + '_tmp_'
            os.mkdir(dir_path)
            paths = []
            n_sample = 0
            nums = {}
            for i, df in enumerate(pool.imap_unordered(self.derivate, dfs)):
                if origin_columns is None:
                    origin_columns = df.columns
                # 用于计算缺失率
                n_sample += df.shape[0]
                for k, v in df.notna().sum().items():
                    if k not in nums:
                        nums[k] = v
                    else:
                        nums[k] += v
                path = os.path.join(dir_path, '{}.zip'.format(i))
                paths.append(path)
                df.to_csv(path, index=False)
                bar.update()
                bar.set_postfix({'num of columns': len(nums)})
        na_rate = {k: 1 - v / n_sample for k, v in nums.items()}
        temp = {k for k, v in na_rate.items() if v < dropna}
        columns = []
        # 保持原始字段的位置在最前
        for col in origin_columns:
            if col in temp:
                columns.append(col)
        columns += temp.difference(columns)
        with open(dst, 'w') as file, tqdm(disable=disable, desc='stage 2') as bar:
            header = True
            for path in paths:
                df = pd.read_csv(path)
                df[list(temp.difference(df.columns))] = None
                df = df[columns]
                df.to_csv(file, index=False, header=header)
                header = False
                os.remove(path)
                bar.update()
                bar.set_postfix({'num of columns': len(columns)})
            shutil.rmtree(dir_path)
        return na_rate
