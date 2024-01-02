"""
processs FASTQ 
"""
from Bio import SeqIO
import os
import numpy as np
import re
from typing import Iterable

from utils.iterator import Iterator

class FASTQ:
    def __init__(self):
        self.dir_cache = os.environ.get('DIR_CACHE')

    def read_fq(self, fq_file:str)->Iterable:
        '''
        ID: rec.id,
        sequence: rec.seq
        phred quality: rec.letter_annotations["phred_quality"]
        Q=-10log _{{10}}P. Q=10->accuracy=90%, Q=20->accuracy=99%
        '''
        for rec in SeqIO.parse(fq_file, 'fastq'):
            # print(rec.id, rec.seq, rec.letter_annotations["phred_quality"])
            yield rec

    def read_pair(self, fq1_file:str, fq2_file:str)->Iterable:
        fq1 = self.read_fq(fq1_file)
        fq2 = self.read_fq(fq2_file)
        for rec1, rec2 in zip(fq1, fq2):
            yield(rec1, rec2)

    def quality_scores(self, rec_iter:Iterable, scores_file:str=None, \
            compress:int=None):
        '''
        phred-quality score: 0-60
        export scores matrix
        '''
        if scores_file is None:
            scores_file = os.path.join(self.dir_cache, "quality_scores.txt")
        if compress is None:
            compress = 10
        # retrieve phred scores
        with open(scores_file, 'wt') as f:
            pool = []
            for rec in rec_iter:
                phred_scores = rec.letter_annotations["phred_quality"]
                if len(pool) < compress:
                    pool.append(phred_scores)
                elif len(pool) == compress:
                    Iterator.shape_length(pool, 0)
                    pool = np.array(pool).mean(axis=0)
                    pool = [ "{:.2f}".format(i) for i in pool]
                    scores = '\t'.join([str(i) for i in pool])
                    f.write(f"{scores}\n")
                    pool = []
            else:
                if len(pool) > 0:
                    Iterator.shape_length(pool, 0)
                    pool = np.array(pool).mean(axis=0)
                    pool = [ "{:.2f}".format(i) for i in pool]
                    scores = '\t'.join([str(i) for i in pool])
                    f.write(f"{scores}\n")
        return scores_file

    def trim_polyx(self, tails:list, min_len:int=None):
        '''
        polyX could be polyA or polyG at 3-end
        args: tails could be ['A', 'G']
        '''
        # polyA most 20~250 nt
        if min_len is None:
            min_len = 15

    def is_fastq(self, fq_file:str)->bool:
        '''
        1. file extension is .fastq, or .fq
        2. file exists
        '''
        extension = os.path.basename(fq_file).split('.')[-1]
        if not extension in ('fastq', 'fq'):
            return False
        if not os.path.isfile(fq_file):
            return False
        return True

    def read_fq0(self):
        '''
        Takes a FASTQ file and returns dictionary of lists
        readDict {'name_root':['full_header', seq, quality]...}
        '''
        readDict = {}
        lineNum, lastPlus, lastHead, skip = 0, False, '', False
        for line in open(self.fastq_file):
            line = line.rstrip()
            if not line:
                continue
            if lineNum % 4 == 0 and line[0] == '@':
                name = line[1:].split()[0]
                readDict[name], lastHead = [], name
            if lineNum % 4 == 1:
                readDict[lastHead].append(line)
            if lineNum % 4 == 2:
                lastPlus = True
            if lineNum % 4 == 3 and lastPlus:
                avgQ = sum([ord(x)-33 for x in line])/len(line)
                sLen = len(readDict[lastHead][-1])
                if avgQ >= self.par['quality_cutoff'] and sLen >= self.par['read_length_cutoff']:
                    readDict[lastHead].append(line)
                    readDict[lastHead] = tuple(readDict[lastHead])
                else:
                    del readDict[lastHead]
                lastPlus, lastHead = False, ''
            lineNum += 1
        return readDict

    def write_fq0(self, adapter_dict, reads, outdir):
        success = 0
        os.system('mkdir ' + self.par['dir_results']  + '/splint_reads')
        for read in reads:
            name, sequence, quality = read, reads[read][0], reads[read][1]
            adapter_plus = sorted(adapter_dict[name]['+'],key=lambda x: x[1], reverse=True)
            adapter_minus=sorted(adapter_dict[name]['-'], key=lambda x: x[1], reverse=True)
            plus_list_name, plus_list_position = [], []
            minus_list_name, minus_list_position = [], []

            for adapter in adapter_plus:
                if adapter[0] != '-':
                    plus_list_name.append(adapter[0])
                    plus_list_position.append(adapter[2])
            for adapter in adapter_minus:
                if adapter[0] != '-':
                    minus_list_name.append(adapter[0])
                    minus_list_position.append(adapter[2])

            if len(plus_list_name) > 0 or len(minus_list_name) > 0:
                success += 1
                splint_file = outdir + 'splint_reads/' + str(int(success/4000)) + '/R2C2_raw_reads.fastq'
                try:
                    out_fastq = open(splint_file, 'a')
                except:
                    os.system('mkdir ' + self.par['dir_results']  + '/splint_reads/' + str(int(success/4000)))
                    out_fastq = open(splint_file, 'w')
                    list_pos=  str(plus_list_position[0]) if len(plus_list_name) > 0 else str(minus_list_position[0])
                    out_fastq.write('@' + name + '_' + list_pos + '\n' + sequence + '\n+\n' + quality + '\n')
            else:
                no_splint_file = outdir + 'splint_reads/No_splint_reads.fastq'
                try:
                    out_fastq = open(no_splint_file, 'a')
                except:
                    out_fastq = open(no_splint_file, 'w')
                    out_fastq.write('>' + name + '\n' + sequence + '\n+\n' + quality + '\n')

    def demultiplexing(self, indir):
        pass
