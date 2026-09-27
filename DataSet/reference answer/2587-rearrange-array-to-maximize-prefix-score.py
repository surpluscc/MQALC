class Solution:
    def maxScore(self, nums: List[int]) -> int:
        nums.sort(reverse=True)
        return sum(s > 0 for s in accumulate(nums))