"""
process DNA sequence using naive methods
"""
from typing import Iterable
from .dna import DNA
from .model.scan import Scan

class Palindromic(DNA):

    def __init__(self, seq:str=None):
        super(Palindromic, self).__init__(seq)

    def detect_longest_palindromic(self)->list:
        if self.length() > 2:
            for palindromic_len in range(self.length(), 2, -1):
                palindromic = self.detect_palindromic(palindromic_len)
                if palindromic:
                    return palindromic
        return []

    def detect_palindromic(self, palindromic_len:int)->list:
        '''
        given sequence length, 
        '''
        pool = []
        iter = Scan.k_mers(self.seq, palindromic_len)
        for sub_seq in iter:
            if Palindromic.is_palindromic(sub_seq[0]):
                pool.append(sub_seq)
        return pool

    @staticmethod
    def is_palindromic(seq:str, iter:str=None)->bool:
        if iter is None: iter = 0
        if len(seq) >= 2:
            first, last = seq[0], seq[-1]
            if first == last:
                return Palindromic.is_palindromic(seq[1:-1], iter+1)
            return False
        else:
            if iter == 0:
                return False
        return True

