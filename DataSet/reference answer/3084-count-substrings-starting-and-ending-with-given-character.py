class Solution:
    def countSubstrings(self, s: str, c: str) -> int:
        return comb(s.count(c) + 1, 2)