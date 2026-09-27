class Solution:
    def lengthOfLongestSubsequence(self, nums: List[int], target: int) -> int:
        f = [0] + [-inf] * target
        s = 0
        for x in nums:
            s = min(s + x, target)
            for j in range(s, x - 1, -1):
                t = f[j - x] + 1
                if t > f[j]:  # 手写 max 效率更高
                    f[j] = t
        return f[-1] if f[-1] > 0 else -1