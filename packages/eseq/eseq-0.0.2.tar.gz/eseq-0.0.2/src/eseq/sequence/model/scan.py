"""
"""
from typing import Iterable
from itertools import islice

class Scan:

    @staticmethod
    def forward(seq:str, start:int=None, step:int=None)->Iterable:
        if start is None or start <= 0: start = 0
        if step is None or step <= 0: step = 1
        end_pos = start
        seq = seq[start:]
        while len(seq) > 0:
            # print(seq, start)
            i = seq[:step]
            end_pos += len(i)
            seq = seq[step:]
            yield (i, end_pos)

    @staticmethod
    def backward(seq:str, step:int=None)->Iterable:
        if step is None or step <= 0: step = 1
        while len(seq) > 0:
            i = seq[-step:]
            seq = seq[:-step]
            yield i 

    @staticmethod
    def neighbor_forward(seq:str, step:int=None)->Iterable:
        '''
        return (n)th, (n+step)th at a time
        '''
        if step is None or step <= 0: step = 1
        while len(seq) > 1:
            a, b = seq[:step], seq[1:(step+1)]
            seq = seq[step:]
            yield a, b


    @staticmethod
    def biends(seq:str)->Iterable:
        while len(seq) >= 2:
            a, b = seq[0], seq[-1]
            seq = seq[1:-1]
            yield a, b
    
    @staticmethod
    def k_mers(seq:str, k:int, start:int=None) -> Iterable:
        '''
        k-mers are substrings of length k contained within a sequence
        '''
        len_seq = len(seq)
        if k <= 0:
            k = 1
        elif k > len_seq:
            k = len_seq
        if start is None or abs(start) >= len_seq:
            start = 0
        elif start < 0:
            start += len_seq
        # iteration
        for start in range(start, len_seq - k + 1):
            subseq = seq[start:start + k]
            # print(k, subseq, start, start+k-1)
            yield (subseq, start, start + k - 1)