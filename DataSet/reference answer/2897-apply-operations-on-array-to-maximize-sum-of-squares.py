class Solution:
    def maxSum(self, nums: List[int], k: int) -> int:
        m = max(nums).bit_length()
        cnt = [0] * m
        for x in nums:
            for i in range(m):
                cnt[i] += x >> i & 1
        ans = 0
        for _ in range(k):
            x = 0
            for i in range(m):
                if cnt[i]:
                    cnt[i] -= 1
                    x |= 1 << i
            ans += x * x
        return ans % (10 ** 9 + 7)