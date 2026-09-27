class Solution:
    def minimizeSum(self, a: List[int]) -> int:
        a.sort()
        return min(a[-3] - a[0], a[-2] - a[1], a[-1] - a[2])