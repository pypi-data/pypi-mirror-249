"""
process DNA sequence using bioPython
"""
from Bio.Seq import Seq

class BioDNA(Seq):
    def __init__(self, seq:str=None, len:int=None):
        super(BioDNA, self).__init__(seq, len)
    
  
    def locate_subseq(self, sub_str:str):
        '''
        index 0-...
        '''
        return self.seq.find(sub_str)