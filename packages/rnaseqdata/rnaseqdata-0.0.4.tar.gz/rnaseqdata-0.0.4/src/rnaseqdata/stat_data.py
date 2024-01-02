
'''
One set of data shall include many samples.
One sample may contain many variables or features
'''
import pandas as pd

class StatData:
    def __init__(self, axis:int=None) -> None:
        '''
        data: dict
        Note: index/column names must be unique
        '''
        self.axis = 1 if axis else 0
        self.data = {}

    def put(self, stat_name:str, input:pd.Series=None):
        '''
        update or create
        '''
        _data = pd.Series(None, dtype='float') if input is None else pd.Series(input)
        _data.name = stat_name
        self.data[stat_name] = _data

    def to_df(self, key1:list=None, stat_names:list=None):
        '''
        export Data as dataframe
        '''
        if not self.data:
            return pd.DataFrame(None, dtype='float')

        # pd.series in list
        _data = {}
        if stat_names:
            for k in stat_names:
                if k in self.data:
                    _data[k] = self.data[k]
                else:
                    n = pd.Series(None, dtype='float')
                    n.name = k
                    _data[k] = n
        else:
            _data = self.data
        # convert
        df = pd.concat(_data.values(), axis=1)
        if key1:
            df = df.reindex(key1)
        df = df.fillna(0).transpose() if self.axis == 1 else df.fillna(0)
        return df


    
