class Solution:
    def maximumStrength(self, nums: List[int], k: int) -> int:
        n = len(nums)
        s = list(accumulate(nums, initial=0))
        f = [0] * (n + 1)
        for i in range(1, k + 1):
            pre = f[i - 1]
            f[i - 1] = mx = -inf
            w = (k - i + 1) * (1 if i % 2 else -1)
            for j in range(i, n - k + i + 1):
                mx = max(mx, pre - s[j - 1] * w)
                pre = f[j]
                f[j] = max(f[j - 1], s[j] * w + mx)
        return f[n]