class Solution:
    def minIncrementOperations(self, nums: List[int], k: int) -> int:
        f0 = f1 = f2 = 0
        for x in nums:
            inc = f0 + max(k - x, 0)
            f0 = min(inc, f1)
            f1 = min(inc, f2)
            f2 = inc
        return f0