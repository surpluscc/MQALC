class Solution:
    def countSubarrays(self, nums: List[int], k: int) -> int:
        ans = left = right = 0
        for i, x in enumerate(nums):
            for j in range(i - 1, -1, -1):
                if nums[j] & x == nums[j]:
                    break
                nums[j] &= x
            while left <= i and nums[left] < k:
                left += 1
            while right <= i and nums[right] <= k:
                right += 1
            ans += right - left
        return ans