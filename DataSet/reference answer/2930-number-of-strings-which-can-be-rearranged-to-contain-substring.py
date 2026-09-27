class Solution:
    def stringCount(self, n: int) -> int:
        MOD = 10 ** 9 + 7
        return (pow(26, n, MOD)
              - pow(25, n - 1, MOD) * (75 + n)
              + pow(24, n - 1, MOD) * (72 + n * 2)
              - pow(23, n - 1, MOD) * (23 + n)) % MOD