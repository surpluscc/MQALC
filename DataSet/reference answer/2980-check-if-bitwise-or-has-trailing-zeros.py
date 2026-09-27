class Solution:
    def hasTrailingZeros(self, nums: List[int]) -> bool:
        return len(nums) - sum(x % 2 for x in nums) >= 2