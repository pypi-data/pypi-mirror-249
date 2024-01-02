'''
create random node data
'''
import numpy as np
import pandas as pd

from .root_data import RootData
from .seq_data import SeqData

class RandomData:

    def __init__(self, sample_num:int, gene_num:int):
        self.sample_num = sample_num
        self.gene_num = gene_num

    def normal_seqdata(self):
        root = RootData(
            samples = self.sample_info(),
            variables = self.gene_annot(),
        )
        seq_data = SeqData(root)
        seq_data.put_data('normRC', self.norm_X())
        return seq_data

    def sample_names(self):
        return [f"sample_{i}" for i in range(1, self.sample_num + 1)]

    def sample_info(self) -> dict:
        samples = {
            'sample_name': self.sample_names(),
            'age': np.random.randint(1,90, size=self.sample_num),
            'gender': np.random.choice(['F', 'M', 'U'], size=self.sample_num),
            'level': np.random.randint(1, 4, size=self.sample_num),
        }
        return samples

    def gene_names(self):
        return [f"gene_{i}" for i in range(1, self.gene_num + 1)]

    def gene_annot(self) -> dict:
        annot = {
            'gene_name': self.gene_names(),
            'start': np.random.randint(1, 999999, size=self.gene_num),
        }
        return annot

    def norm_X(self):
        '''
        suppose log2 of normRC follows the distribution of Gussain(0,1)
        '''
        _data = np.random.normal(size=(self.sample_num, self.gene_num))
        X= pd.DataFrame(
            2**_data,
            index=self.sample_names(),
            columns=self.gene_names(),
            dtype = 'float'
        )
        return X


       