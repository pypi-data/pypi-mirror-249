"""
detect ORF open reading frame
ORF: protein coding region
gene sequence translated into protein
1. ORF = start_codon + sequences uninterrupted by stop codons
2. may include 5'-UTR and introns and 3'UTR.
"""
from typing import Iterable
from .dna import DNA
from .model.scan import Scan

class ORF(DNA):
    def __init__(self, seq:str=None, min_length:int=None, ignore_nested:bool=None):
        # DNA sequence
        super(ORF, self).__init__(seq)
        # minimal ORF length (nt)
        self.min_length = 30 if min_length is None else min_length
        # ignore nested ORFs
        self.ignore_nested = True if ignore_nested is None else False
        # store all ORFs
        self.orfs = []

    def is_start_codon(self, codon:str)->bool:
        '''
        '''
        start_codons = {'ATG', }
        if codon in start_codons:
            return True
        return False

    def detect_start_codon(self)->Iterable:
        '''
        search all start codon
        '''
        for codon, start, end in Scan.k_mers(self.seq, 3):
            if self.is_start_codon(codon):
                yield (codon, start, end)

    def is_termination_codon(self, codon:str)->bool:
        '''
        '''
        termination_codons = {'TAA', 'TAG', 'TGA'}
        if codon in termination_codons:
            return True
        return False

    def detect_termination_codon(self, start:int)->tuple:
        '''
        args: start=index of start codon or the nt after start codon
        '''
        for codon, end_pos in Scan.forward(self.seq, start, 3):
            # print(codon, end_pos)
            if self.is_termination_codon(codon):
                if (end_pos - start) >= self.min_length:
                    termination_codon = (codon, end_pos-3, end_pos)
                    # print(termination_codon)
                    return termination_codon
        return None
            
    def is_nested_orf(self, new_orf)->bool:
        for orf_start, orf_end in self.orfs:
            if new_orf[0]>=orf_start and new_orf[1]<=orf_end:
                return True
        return False

    def detect_orfs(self):
        '''
        suppose there is no intron.
        '''
        for start_codon in self.detect_start_codon():
            termination_codon = self.detect_termination_codon(start_codon[1])
            # print(start_codon, termination_codon)
            if termination_codon:
                orf = (start_codon[1], termination_codon[2])
                if orf not in self.orfs:
                    if (not self.ignore_nested) or (self.ignore_nested \
                        and not self.is_nested_orf(orf)):
                        self.orfs.append(orf)
        # print([(self.seq[a:b],a,b) for a,b in self.orfs])
        return self.orfs