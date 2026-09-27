class Solution:
    def missingInteger(self, nums: List[int]) -> int:
        s = nums[0]
        for x, y in pairwise(nums):
            if x + 1 != y: break
            s += y

        st = set(nums)
        while s in st:  # 至多循环 n 次，例如 1324567
            s += 1
        return s