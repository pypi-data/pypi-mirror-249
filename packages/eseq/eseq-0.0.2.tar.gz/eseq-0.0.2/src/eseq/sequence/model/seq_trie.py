"""
split sequence into nodes
basic unit of a trie
"""
class Node:
    def __init__(self, val:str=None):
        self.val = val if val is not None else ''
        self.is_leave = False
        # distance between this node to root node
        self.depth = 0
        #root node has not father
        # other nodes have only one father
        self.father = None
        # leave nodes have no children
        # other nodes have one or many children
        self.children = {}
        # the two attr used for locating seq
        # index of this node in the entire sequence
        self.val_pos = ()

    def child_node(self, child_val:str):
        children = getattr(self, 'children')
        if child_val in children:
            return children[child_val]
        return None

    def father_node(self):
        return getattr(self, 'father')
    
    def is_leave_node(self)->bool:
        return self.is_leave


"""
store long sequence into a trie
slice long sequence into many seqs
one seq is stored into the trie
"""
from typing import Iterable
from .scan import Scan

class SeqTrie:
    def __init__(self, root_val:str=None):
        # mostly, root node has no value
        # sometimes all sequences share identifical prefix
        self.root = Node(root_val)
        self.seq_nodes = ()

    def insert(self, seq:str, end_pos:int=None)->Node:
        '''
        args: val is sequence namely A/T/G/C
        '''
        # print('###', seq)
        curr_node = self.root
        for val in seq:
            if val not in curr_node.children:
                # print(val)
                this_node = Node(val)
                this_node.depth = curr_node.depth + 1
                this_node.father = curr_node
                curr_node.children[val] = this_node
                curr_node = this_node
            else:
                curr_node = curr_node.children[val]
        else:
            curr_node.is_leave = True
            if end_pos:
                curr_node.val_pos += (end_pos,)
        self.seq_nodes += (curr_node,)
        return curr_node

    def dfs_search(self, curr_node:Node, prefix:str)->Iterable:
        '''
        retrieve entrie sequence from trie
        '''
        # print(prefix, curr_node.val)
        prefix += curr_node.val
        if curr_node.is_leave:
            yield prefix, curr_node.val_pos
        else:
            for child_node in curr_node.children.values():
                yield from self.dfs_search(child_node, prefix)

    def scan(self)->Iterable:
        '''
        retrieve sequence slices from trie
        Note: order of slices may differ from origin sequence
        '''
        curr_node = self.root
        for seq, _ in self.dfs_search(curr_node, ''):
            yield seq


    def get(self, leave_node:Node)->str:
        '''
        get seq slice based on reference of leave node
        '''
        seq = ''
        curr_node = leave_node
        while hasattr(curr_node, 'father'):
            seq = curr_node.val + seq
            curr_node = curr_node.father
        return seq
    
    def retrieve(self)->Iterable:
        '''
        retrieve seq
        '''
        for leave_node in self.seq_nodes:
            yield self.get(leave_node)

    def insert_sequence(self, sequence:str, layers:int=None):
        '''
        split long sequence into slices which are inserted into Trie
        '''
        if layers is None or layers < 1: layers = 10
        for seq, end_pos in Scan.forward(sequence, 0, layers):
            self.insert(seq, end_pos)

    def get_sequence(self)->str:
        '''
        retrieve entrie sequence from trie
        Note: not recommended if sequence is long
        '''
        sequence = ()
        for leave_node in self.seq_nodes:
            sequence += (self.get(leave_node),)
        return ''.join(sequence)



