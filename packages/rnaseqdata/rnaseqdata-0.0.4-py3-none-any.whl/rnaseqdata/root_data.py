'''
1. Root data only store sample information and features/variables
2. root data doesn't defines counting data
3. root data should be ancestor of all other nodes
'''

from .annot_data import AnnotData

class RootData:
    is_root = True

    def __init__(self, samples:dict=None, variables:dict=None):
        self.samples = AnnotData(0, samples)
        self.variables = AnnotData(1, variables)
        self.children = []
            
