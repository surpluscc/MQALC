class Solution:
    def separateDigits(self, nums: List[int]) -> List[int]:
        ans = []
        for x in reversed(nums):
            while x:
                ans.append(x % 10)
                x //= 10
        ans.reverse()  # 原地反转
        return ans