'''
independent data in matrix
samples in rows, variables in columns
'''
import pandas as pd
import json

from .stat_data import StatData
from .root_data import RootData


class NodeData:
    is_root = False

    def __init__(self, parent:RootData, name:str, X:pd.DataFrame=None):
        self.parent, self.children = parent, []
        parent.children.append(self)
        self.name = name if name else 'default'
        # X: sort and fill NA
        self.X = pd.DataFrame(X).sort_index(axis=0).sort_index(axis=1).fillna(0)
        # cross rows
        self.samples = parent.samples
        self.row_stat = StatData(axis=0)
        # cross columns
        self.variables = parent.variables
        self.col_stat = StatData(axis=1)

    def get_root(self):
        if self.parent:
            return self.parent.get_root()
        return self

    def row_labels(self, labels:set=None) -> pd.DataFrame:
        key1 = list(self.X.index)
        # stat data
        stat_names = set(self.row_stat.data)
        stat_labels = stat_names.intersection(labels) if labels else []
        _stat = self.row_stat.to_df(key1, list(stat_labels),)
        # annot data
        annot_labels = list(labels.difference(stat_names)) if labels else []
        _annot = self.samples.to_df(key1, list(annot_labels),)
        return pd.concat([_annot, _stat], axis=1).fillna('-')

    def col_labels(self, labels:set=None) -> pd.DataFrame:
        key1 = list(self.X)
        # stat data
        stat_names = set(self.col_stat.data)
        stat_labels = stat_names.intersection(labels) if labels else []
        _stat = self.col_stat.to_df(key1, list(stat_labels),)
        # annot data
        annot_labels = list(labels.difference(stat_names)) if labels else []
        _var = self.variables.to_df(key1, list(annot_labels),)
        return pd.concat([_var, _stat], axis=0).fillna('-')

    def put_data(self, new_data:pd.Series):
        '''
        index names of series are columns names
        '''
        # remove duplicates and sort by index name
        new_data = new_data[~new_data.index.duplicated()].sort_index()
        # confirm name of series
        if not new_data.name:
            new_data.name = self.X.shape[0] + 1
        row_name = new_data.name

        # update row
        if row_name in list(self.X.index):
            _data = NodeData.combine_series(self.X.loc[row_name], new_data)
            self.X.loc[row_name, _data.index] = _data
        #Or add new row
        else:
            _data = pd.DataFrame(new_data).T
            self.X = pd.concat([self.X, _data], axis=0)
        self.X = self.X.fillna(0)
        return self.X.loc[row_name]

    @staticmethod
    def combine_series(s1:pd.Series, s2:pd.Series) -> pd.Series:
        def func(x, y):
            _x = 0 if str(x) == 'nan' else x
            _y = 0 if str(y) == 'nan' else y
            return _x + _y
        return s1.combine(s2, func)

    def to_df_samples(self, labels:set=None) -> pd.DataFrame:
        # add sample data to the left side
        _data = self.row_labels(labels)
        if not _data.empty:
            _data = pd.concat([_data, self.X], axis=1)
            return _data
        return self.X

    def to_df_variables(self, labels:set=None) -> pd.DataFrame:
        # add features data to the top side
        _data = self.col_labels(labels)
        if not _data.empty:
            _data = pd.concat([_data, self.X], axis=0)
            return _data
        return self.X