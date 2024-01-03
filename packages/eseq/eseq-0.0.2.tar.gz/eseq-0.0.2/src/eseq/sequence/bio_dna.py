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
    
    def nt_bitvector(self) -> dict:
        '''
        key-value: reversed bitset of positions
        '''
        def bitset(seq, mask, mask_len):
            if not seq:
                return mask
            letter = seq[0]
            tag = 0
            for k in list(mask):
                if k == letter:
                    mask[k] += 2 ** mask_len
                    tag = 1
                    break
            if tag == 0:
                mask[letter] = 2 ** mask_len
            return bitset(seq[1:], mask, mask_len + 1)

        #
        mask_len = self.__len__()
        mask = bitset(self, {}, 0)
        mask_str = dict([(k, format(v, f'0{mask_len}b')) for k,v in mask.items()])
        return mask, mask_str

    def format_code(self, code:int):
        return format(code, f"0{self.len}b")
  
    def shift_and(self, text:str, first_occurrence:bool=False):
        '''
        exact match pattern: Shift-and
        '''
        pattern, _ = self.nt_bitvector()
        pattern_len = self.__len__()

        p, res = 0, []
        target = 2 ** (pattern_len - 1)
        for i, v in enumerate(text):
            v_code = pattern.get(v, 0)
            p = (p << 1 | 1) & v_code
            # print(self.format_code(v_code), self.format_code(p))
            if p >= target:
                res.append(i - pattern_len + 1)
                if first_occurrence:
                    return res
        return res