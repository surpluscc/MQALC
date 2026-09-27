class Solution:
    def minOperationsToMakeMedianK(self, nums: List[int], k: int) -> int:
        nums.sort()
        m = len(nums) // 2
        ans = 0
        if nums[m] > k:
            for i in range(m, -1, -1):
                if nums[i] <= k:
                    break
                ans += nums[i] - k
        else:
            for i in range(m, len(nums)):
                if nums[i] >= k:
                    break
                ans += k - nums[i]
        return ans