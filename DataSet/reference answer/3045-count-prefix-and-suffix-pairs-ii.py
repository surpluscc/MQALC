class Node:
    __slots__ = 'son', 'cnt'

    def __init__(self):
        self.son = dict()
        self.cnt = 0

class Solution:
    def countPrefixSuffixPairs(self, words: List[str]) -> int:
        ans = 0
        root = Node()
        for s in words:
            cur = root
            for p in zip(s, reversed(s)):
                if p not in cur.son:
                    cur.son[p] = Node()
                cur = cur.son[p]
                ans += cur.cnt
            cur.cnt += 1
        return ans