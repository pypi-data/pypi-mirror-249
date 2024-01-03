from Bio.Seq import Seq

class RNA(Seq):
    def __init__(self, seq:str=None, len:int=None):
        super(RNA, self).__init__(seq, len)