class Solution:
    def findScore(self, nums: List[int]) -> int:
        ans = 0
        i, n = 0, len(nums)
        while i < n:
            i0 = i
            while i + 1 < n and nums[i] > nums[i + 1]:  # 找到下坡的坡底
                i += 1
            for j in range(i, i0 - 1, -2):  # 从坡底 i 到坡顶 i0，每隔一个累加
                ans += nums[j]
            i += 2  # i 选了 i+1 不能选
        return ans