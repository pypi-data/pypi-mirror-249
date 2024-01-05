# ernav2_seqdata
A new data type known as SeqData is designed for RNA-seq data analysis. The data type is designed for data integration from various sources and dimensions:

<img src="static/mrnaseq_data.png" width="900" height="250">

Expression of RNA is measured by read counts of transcripts. A typical bioinformatics pipeline of mRNA-seq determines reads counts (RC) of transcripts. The RCs are typically 2-D table, of which samples are in rows, and transcripts (or genes) are in columns, or in the reverse. After that, the RC table would be normalized as FPM or FPKM or somewhere else by a certain normalized method. The next, co-founding factors among samples would be removed using a certain method namely DESEQ2 or EdgeR etc. Moreover, those data would be transformed into various table, namely log, or partitioned into some subset. Bioinformatician should manage all those data sets during statistical anlaysis.

<img src="static/SeqData.png" width="600" height="400">

Biological scientists may be more care about significance of mRNA-seq data analysis, and what those significance reveals. In this case, sample informations, or patient information, or features of samples (namely single cells) shall be considered. Moreover, aside from transcript ID or Gene ID, other annotations would be integrated, for example, genomic annoations namely chromosome locus, protein annotations namely domain identification would be integrated, too. Those annoation data may not be used in statistical process, but really needed for further study.

SeqData is tree structure. The root contains data of phenotypes and annotations. Each node contains various attributes including X in m x n, and var (statistical aggregations). Nodes inherite the attributes of the root nodes. Data of children nodes is determined by those of parent nodes.

<img src="static/SeqData_data_structure.png" width="350" height="300">

## installation
It is convenient to install the repository using pip. The package could be found at [Pythone Package Index](https://pypi.org/manage/project/rnaseqdata/releases/).
```
pip install --upgrade rnaseqdata
```

## Development
```
git clone git@github.com:Tiezhengyuan/ernav2_seqdata.git
cd ernav2_seqdata
```

create virtual environment
```
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
```


Unit testing
```
pytest tests/unittests
```

## quick tourial
In Python3

```
from rnaseqdata import RootData, SeqData
import numpy as np
import pandas as pd
```

Create SeqData

```
root = RootData()
c = SeqData(root)
c.put_data('test', np.eye(3), root)
c.to_df('test)
```

          0    1    2
     0  1.0  0.0  0.0
     1  0.0  1.0  0.0
     2  0.0  0.0  1.0

