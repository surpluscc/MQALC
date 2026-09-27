class Solution:
    def countWays(self, nums: List[int]) -> int:
        n = len(nums)
        res = 0
        nums.sort()
        for k in range(0, n + 1):
            # 前 k 个元素的最大值是否小于 k
            if k > 0 and nums[k - 1] >= k:
                continue
            # 后 n - k 个元素的最小值是否大于 k
            if k < n and nums[k] <= k:
                continue
            res += 1
        return res