"""
PROSITE fingerprints are described by regular expressions
https://prosite.expasy.org/prosuser.html#conv_pa
"""
import re

class Prosite:
    def __init__(self, prosite:str):
        self.prosite = prosite.upper()
        self.regexp_obj = None
    
    def motif_length(self)->int:
        '''
        determine motif length
        '''
        min_len, max_len = 0, 0
        for aa in self.prosite.split('-'):
            repeat = re.findall(r'\((\d+)\)', aa)
            if repeat:
                i = int(repeat[0])
                min_len += i
                max_len += i
            else:
                if re.findall(r'\[.*\]|\{.*\}', aa):
                    min_len += 1
                    max_len += 1
                else:
                    repeat = re.findall(r'(\w+)\((\d+,\d+)\)', aa)
                    # print(aa, repeat)
                    if repeat:
                        a,b = [int(i) for i in repeat[0][1].split(',')]
                        min_len += a * len(repeat[0][0])
                        max_len += b * len(repeat[0][0])
                    else:
                        min_len += len(aa)
                        max_len += len(aa)
        return min_len, max_len

    def compile_prosite(self):
        '''
        convert prosite to regexp and compile it into re_obj
        '''
        res = self.prosite
        res = res.replace(r'{', '[^').replace(r'}', ']')
        # repeats
        res = res.replace('(', '{').replace(')', '}')
        # N-terminal or C-terminal
        res = res.replace('<', '^').replace('>', '$')
        # any amino acids
        res = res.replace('X', r'\w')
        res = res.replace(r'-', '')
        # print(res)
        self.regexp_obj = re.compile(res)
        return self.regexp_obj

    def search_motif(self, protein:str):
        """
        search all motifs given a protein sequence
        """
        self.compile_prosite()

        if self.regexp_obj:
            protein = protein.upper()
            pool = []
            for m in re.finditer(self.regexp_obj, protein):
                # index of start, end, and matched motif
                res = (m.start(), m.end(), m.group())
                pool.append(res)
            return pool
