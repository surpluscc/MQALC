class Solution:
    def selfDivisiblePermutationCount(self, n: int) -> int:
        m = (1 << n) - 1
        @cache
        def dfs(i, mask):
            if mask == m:return 1
            return sum(dfs(i + 1, mask | (1 << j)) for j in range(n) if (mask >> j) & 1 == 0 and gcd(n - j, i) == 1)
        return dfs(1, 0)