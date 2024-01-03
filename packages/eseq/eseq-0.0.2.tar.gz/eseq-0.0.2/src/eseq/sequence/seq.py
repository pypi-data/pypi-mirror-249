"""
process sequence
"""
from typing import Iterable, Callable

class Seq:
    def __init__(self, seq:str=None):
        self.seq = seq.upper().replace('\n', '') if \
            seq and isinstance(seq, str) else ''
    
    def length(self)->int:
        return len(self.seq)

    def reverse(self)->str:
        return self.seq[::-1]
    
    def count_sub_seq(self, sub_seq:str)->list:
        if len(sub_seq)==0:
            return 0
        return self.seq.count(sub_seq)

    def count_occurrence(self)->dict:
        res = {}
        for i in self.seq:
            if i in res:
                res[i] += 1
            else:
                res[i] = 1
        return res
    
    def search_sub_seq(self, sub_seq:str)->list:
        '''
        search all subsequences 
        '''
        if len(sub_seq)==0:
            return []
        #
        count, start = [], 0
        while start != -1:
            pos = self.seq.find(sub_seq, start)
            if pos >= 0:
                end = pos + len(sub_seq)
                count.append((pos, end))
                start += end
            else:
                start = -1
        return count
        
    def calculate_hamming_distance(self, seq2:str, func:Callable=None)->int:
        '''
        number of positions of that two codewords of the same length differe
        Note: self.seq and seq2 may be same lengths
        '''
        if func is None:
            def func(a, b):
                return a != b
        #
        dist = 0
        for a,b in zip(self.seq, seq2):
            if func(a, b):
                dist += 1
        dist += abs(len(self.seq)-len(seq2))
        return dist
        
    def calculate_similarity(self, seq2:str)->float:
        '''
        Note: self.seq and seq2 may be same lengths
        '''
        dist = self.calculate_hamming_distance(seq2)
        seq_len = len(self.seq) if len(self.seq) >= len(seq2) else len(seq2)
        return (seq_len - dist)/seq_len

    def match_5end(self, seq2:str) -> int:
        '''
        match from 5'-end
        return distance score
        '''
        dist = 0
        end = len(seq2) if len(seq2) <= len(self.seq) else len(self.seq)
        for i in range(0, end):
            if self.seq[i] == seq2[i]:
                dist += 1
        return dist

