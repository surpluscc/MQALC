class Solution:
    def maxFrequencyScore(self, nums: List[int], k: int) -> int:
        nums.sort()
        ans = left = s = 0  # s 是窗口元素与窗口中位数的差之和
        for right, x in enumerate(nums):
            s += x - nums[(left + right) // 2]
            while s > k:
                s += nums[left] - nums[(left + right + 1) // 2]
                left += 1
            ans = max(ans, right - left + 1)
        return ans