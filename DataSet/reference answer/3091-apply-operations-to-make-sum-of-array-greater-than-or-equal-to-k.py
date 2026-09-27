class Solution:
    def minOperations(self, k: int) -> int:
        rt = max(isqrt(k - 1), 1)
        return min(rt - 1 + (k - 1) // rt, rt + (k - 1) // (rt + 1))