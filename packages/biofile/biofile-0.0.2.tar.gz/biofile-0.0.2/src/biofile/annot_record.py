"""
define annotation record: one recored, and one line in GTF/GFF
"""
import re

class AnnotRecord:
    # column 1-9 in GTF/GFF
    names = ['seqid', 'source', 'feature', 'start', 'end', \
        'score', 'strand', 'phase', 'attributes',]

    def __init__(self):
        self.seqid = None
        self.source = None
        self.feature = None
        self.start = None
        self.end = None
        self.score = None
        self.strand = None
        self.phase = None
        self.attributes = None

    def parse(self, record_line:str):
        items = record_line.split('\t')
        for k,v in zip(self.names, items):
            setattr(self, k, v)
        if self.start:
            self.start = int(self.start)
        if self.end:
            self.end = int(self.end)
        return self

    def parse_gtf_attributes(self):
        '''
        GTF attributes
        '''
        names = re.findall('([a-zA-Z0-9_]+)\\s\"', self.attributes)
        values = re.findall('\"([a-zA-Z0-9_\\.\\%\\:\\(\\)\\-\\,\\/\\s]*?)\"', self.attributes)
        attr = [{'name': k, 'value': v} for k, v in zip(names, values)]
        return attr

    def parse_gff_attributes(self):
        '''
        GFF attributes
        '''
        names = re.findall('([a-zA-Z0-9_]+)=', self.attributes)
        values = re.findall('=([a-zA-Z0-9_\\.\\s\\:\\/\\-\\%\\(\\)\\,\'\\[\\]\\{\\}]+)', self.attributes)
        attr = []
        for k, v in zip(names, values):
            if k == 'Dbxref' and ',' in v:
                for v2 in v.split(','):
                    attr.append({'name': k, 'value': v2})
            else:
                attr.append({'name': k, 'value': v})
        return attr

    def to_dict(self) -> dict:
        return dict([(k, getattr(self, k)) for k in self.names])

    def to_dict_simple(self) -> dict:
        names = ['seqid', 'start', 'end', 'strand',]
        return dict([(k, getattr(self, k)) for k in names])
