class Solution:
    def minImpossibleOR(self, nums: List[int]) -> int:
        mask = 0
        for x in nums:
            if (x & (x - 1)) == 0:  # x 是 2 的幂次
                mask |= x
        mask = ~mask
        return mask & -mask  # lowbit