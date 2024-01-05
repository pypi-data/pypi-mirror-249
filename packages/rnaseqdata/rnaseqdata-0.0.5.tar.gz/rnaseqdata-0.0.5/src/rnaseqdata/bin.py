import pickle
import os
from .root_data import RootData
from .seq_data import SeqData

def load_seqdata(infile:str=None) -> SeqData:
    try:
        if os.path.isfile(infile):
            with open(infile, 'rb') as f:
                seqdata = pickle.load(f)
                return seqdata
    except Exception as e:
        print(f"Failed in read data from {infile}. error={e}")
    
    # create a new SeqData
    root = RootData()
    seqdata = SeqData(root)
    return seqdata

def dump_seqdata(seqdata:SeqData, outfile:str) -> bool:
    try:
        with open(outfile, 'wb') as f:
            pickle.dump(seqdata, f)
        return True
    except Exception as e:
        print(f"Failed in saving {outfile} in pickle format. error={e}")
    return False
