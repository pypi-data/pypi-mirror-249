'''
SeqData(): A container include root and all nodes
'''

import pandas as pd

from .stat_data import StatData
from .root_data import RootData
from .node_data import NodeData


class SeqData:

    def __init__(self, root:RootData=None):
        self.root = root if root else RootData()
        self.nodes = {}
    
    def data_names(self) -> list:
        return list(self.nodes)
    
    def get_node_data(self, data_name:str) -> NodeData:
        return self.nodes.get(data_name)
    
    def put_data(self, name:str, X:pd.DataFrame, parent_name:str=None) -> NodeData:
        '''
        create/update node data
        '''        
        parent = self.nodes.get(parent_name, self.root)
        new_data = NodeData(parent, name, X)
        self.nodes[name] = new_data
        return new_data

    def to_df(self, data_name:str, expand_axis:int=None, labels:set=None):
        expand_axis = 1 if expand_axis else 0
        if data_name in self.nodes:
            node = self.nodes[data_name]
            if expand_axis == 0:
                return node.to_df_samples(labels)
            return node.to_df_variables(labels)
        return None
