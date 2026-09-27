class Solution:
    def scoreOfString(self, s: str) -> int:
        return sum(abs(x - y) for x, y in pairwise(map(ord, s)))