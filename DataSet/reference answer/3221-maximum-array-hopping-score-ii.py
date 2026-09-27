max_ = lambda x, y: x if x> y else y

class Solution:
    def maxScore(self, nums: List[int], ans = 0, mx = 0) -> int:

        for num in nums[-1:0:-1]:
            mx = max_(mx, num)
            ans+= mx

        return ans