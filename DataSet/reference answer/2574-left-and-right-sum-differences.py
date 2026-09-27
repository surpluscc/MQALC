class Solution:
    def leftRightDifference(self, nums: List[int]) -> List[int]:
        left_sum, right_sum = 0, sum(nums)
        for i, x in enumerate(nums):
            right_sum -= x
            nums[i] = abs(left_sum - right_sum)
            left_sum += x
        return nums