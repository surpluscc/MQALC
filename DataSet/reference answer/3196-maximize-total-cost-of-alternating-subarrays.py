class Solution:
    def maximumTotalCost(self, a: List[int]) -> int:
        f0, f1 = 0, a[0]
        for i in range(1, len(a)):
            f0, f1 = f1, max(f1 + a[i], f0 + a[i - 1] - a[i])
        return f1