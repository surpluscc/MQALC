class Solution:
    def sumOfSquares(self, nums: List[int]) -> int:
        ans, n = 0, len(nums)
        for i in range(1, isqrt(n) + 1):
            if n % i == 0:
                ans += nums[i - 1] ** 2  # 注意数组的下标还是从 0 开始的
                if i * i < n:  # 避免重复统计
                    ans += nums[n // i - 1] ** 2
        return ans