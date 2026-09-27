class Solution:
    def lastVisitedIntegers(self, nums: List[int]) -> List[int]:
        ans = []
        seen = []
        k = 0
        for x in nums:
            if x > 0:
                seen.append(x)
                k = 0
            else:
                k += 1
                ans.append(-1 if k > len(seen) else seen[-k])  # 倒数第 k 个
        return ans