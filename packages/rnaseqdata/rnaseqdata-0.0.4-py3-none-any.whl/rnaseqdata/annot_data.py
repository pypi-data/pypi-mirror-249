'''
Data: annotation, sample information or features etc
Data is pd.Series. data type is object
'''
import os
import json
import pandas as pd

class AnnotData:
    def __init__(self, axis:int=None, data:dict=None):
        '''
        axis=0, place data across rows
        axos=1, place data across columns
        '''
        self.axis = 1 if axis else 0
        self.data = pd.Series(data, dtype='object')
    
    def from_json(self, infile:str):
        if not os.file.isfile(infile):
            return None
        with open(infile, 'r') as f:
            _data = pd.Series(json.load(f), dtype='object')
            self.data = self.data.combine_first(_data)
    
    def to_json(self, outfile:str):
        try:
            with open(outfile, 'w') as f:
                _data = self.data.to_dict()
                json.dump(_data, f, indent=4)
                return True
        except Exception as e:
            pass
        return False
    
    def update(self, input):
        '''
        input could be key1 in list type 
        or key1~key2 data in dict type
        '''
        _data = pd.Series(None, index=list(input), dtype='object') if \
            isinstance(input, 'list') else pd.Series(input, dtype='object')
        self.data = self.data.combine_first(_data)

    def to_df(self, key1:list=None, key2:list=None):
        '''
        convert data to data frame
        '''
        _data = self.data.reindex(key1) if key1 else self.data
        _data = _data.map(lambda x: {} if str(x) == 'nan' else x)
        _data = _data.to_dict()
        df = pd.DataFrame.from_dict(_data)
        if key2:
            df = df.reindex(key2).fillna('-')
        if self.axis == 0:
            return df.transpose()
        return df


