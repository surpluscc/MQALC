class Solution:
    def maxScore(self, nums: List[int]) -> int:
        res, mx = 0, 0
        for i in range(len(nums)-1, 0, -1):
            mx = max(mx, nums[i])
            res += mx
        return res