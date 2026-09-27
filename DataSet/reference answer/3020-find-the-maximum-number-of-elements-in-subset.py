class Solution:
    def maximumLength(self, nums: List[int]) -> int:
        cnt = Counter(nums)
        ans = cnt[1] - 1 | 1  # 奇数
        del cnt[1]
        for x in cnt:
            res = 0
            while cnt[x] > 1:
                res += 2
                x *= x
            ans = max(ans, res + (1 if x in cnt else -1))  # 保证 res 是奇数
        return ans