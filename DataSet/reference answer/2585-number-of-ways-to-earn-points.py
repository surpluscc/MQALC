class Solution:
    def waysToReachTarget(self, target: int, types: List[List[int]]) -> int:
        MOD = 1_000_000_007
        f = [1] + [0] * target
        for count, marks in types:
            for j in range(target, marks - 1, -1):
                for k in range(1, min(count, j // marks) + 1):
                    f[j] += f[j - k * marks]
                f[j] %= MOD
        return f[-1]