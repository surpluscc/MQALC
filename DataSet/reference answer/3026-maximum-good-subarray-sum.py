class Solution:
    def maximumSubarraySum(self, nums: List[int], k: int) -> int:
        min_s = defaultdict(lambda: inf)
        s = 0
        ans = -inf
        for x in nums:
            ans = max(ans, s + x - min(min_s[x - k], min_s[x + k]))
            min_s[x] = min(min_s[x], s)
            s += x
        return ans if ans > -inf else 0