"""

"""
from copy import deepcopy
import gzip
import os
import re
import pandas as pd 


class Utils:


    @staticmethod
    def parse_ncbi_acc(infile)->dict:
        '''
        value: NCBI_protein_accession, index: UniProtKB_protein_accession
        source file: *_gene_refseq_uniprotkb_collab.gz
        '''
        accessions = {}
        # infile = os.path.join(self.dir_source, "gene_refseq_uniprotkb_collab.gz")
        df = pd.read_csv(infile, sep='\t', header=0)
        index_name = 'UniProtKB_protein_accession'
        df['acc_group'] = df[index_name].str[:2]
        for name, sub_df in df.groupby(['acc_group']):
            series = None
            if len(sub_df) > 1:
                series = pd.Series(sub_df.iloc['#NCBI_protein_accession'].squeeze())
                series.index = sub_df[index_name]
            elif len(sub_df) == 1:
                series = pd.Series(sub_df.iat[0,0], index=[sub_df.iat[0,1],])
            if series is not None:
                series.index.name = index_name
                series.name = name
                accessions[name] = series
            print(series.shape, series)
            print('\n\n')
        return accessions