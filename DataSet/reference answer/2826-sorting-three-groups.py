class Solution:
    def minimumOperations(self, nums: List[int]) -> int:
        f = [0] * 4
        for x in nums:
            f[x] = max(f[1: x + 1]) + 1
        return len(nums) - max(f)