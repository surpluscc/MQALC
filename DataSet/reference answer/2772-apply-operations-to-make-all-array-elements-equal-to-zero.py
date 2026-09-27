class Solution:
    def checkArray(self, nums: List[int], k: int) -> bool:
        n = len(nums)
        d = [0] * (n + 1)
        sum_d = 0
        for i, x in enumerate(nums):
            sum_d += d[i]
            x += sum_d
            if x == 0: continue  # 无需操作
            if x < 0 or i + k > n: return False  # 无法操作
            sum_d -= x  # 直接加到 sum_d 中
            d[i + k] += x
        return True