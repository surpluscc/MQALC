class Solution:
    def sumOfPower(self, nums: List[int], k: int) -> int:
        f = [1] + [0] * k
        for x in nums:
            for j in range(k, -1, -1):
                f[j] = (f[j] * 2 + (f[j - x] if j >= x else 0)) % 1_000_000_007
        return f[k]