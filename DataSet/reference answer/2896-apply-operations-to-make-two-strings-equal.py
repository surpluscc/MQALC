class Solution:
    def minOperations(self, s1: str, s2: str, x: int) -> int:
        if s1 == s2:
            return 0
        p = [i for i, (x, y) in enumerate(zip(s1, s2)) if x != y]
        if len(p) % 2:
            return -1
        f0, f1 = 0, x
        for i, j in pairwise(p):
            f0, f1 = f1, min(f1 + x, f0 + (j - i) * 2)
        return f1 // 2