class Solution:
    def findPermutation(self, a: List[int]) -> List[int]:
        n = len(a)
        f = [[inf] * n for _ in range(1 << n)]
        g = [[-1] * n for _ in range(1 << n)]
        for j in range(n):
            f[-1][j] = abs(j - a[0])
        for s in range((1 << n) - 3, 0, -2):  # 注意偶数不含 0，是无效状态
            for j in range(n):
                if s >> j & 1 == 0:  # 无效状态，因为 j 一定在 s 中
                    continue
                for k in range(1, n):
                    if s >> k & 1:  # k 之前填过
                        continue
                    v = f[s | 1 << k][k] + abs(j - a[k])
                    if v < f[s][j]:
                        f[s][j] = v
                        g[s][j] = k  # 记录该状态下填了哪个数

        ans = []
        s = j = 0
        while j >= 0:
            ans.append(j)
            s |= 1 << j
            j = g[s][j]
        return ans