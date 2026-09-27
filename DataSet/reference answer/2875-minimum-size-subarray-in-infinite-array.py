class Solution:
    def minSizeSubarray(self, nums: List[int], target: int) -> int:
        total = sum(nums)
        n = len(nums)
        ans = inf
        left = s = 0
        rem = target % total
        for right in range(n * 2):
            s += nums[right % n]
            while s > rem:
                s -= nums[left % n]
                left += 1
            if s == rem:
                ans = min(ans, right - left + 1)
        return ans + target // total * n if ans < inf else -1