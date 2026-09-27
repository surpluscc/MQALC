class Solution:
    def numberOfGoodSubarraySplits(self, nums: List[int]) -> int:
        MOD = 10 ** 9 + 7
        ans, pre = 1, -1
        for i, x in enumerate(nums):
            if x == 0: continue
            if pre >= 0:
                ans = ans * (i - pre) % MOD
            pre = i
        return 0 if pre < 0 else ans