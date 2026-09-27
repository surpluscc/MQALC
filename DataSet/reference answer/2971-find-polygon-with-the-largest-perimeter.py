class Solution:
    def largestPerimeter(self, nums: List[int]) -> int:
        nums.sort()
        ans = -1
        s = 0
        for x in nums:
            s += x
            if s > x * 2:  # s-x > x
                ans = s
        return ans