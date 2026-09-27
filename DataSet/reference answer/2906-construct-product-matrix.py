class Solution:
    def constructProductMatrix(self, grid: List[List[int]]) -> List[List[int]]:
        MOD = 12345
        n, m = len(grid), len(grid[0])
        p = [[0] * m for _ in range(n)]

        suf = 1  # 后缀乘积
        for i in range(n - 1, -1, -1):
            for j in range(m - 1, -1, -1):
                p[i][j] = suf  # p[i][j] 先初始化成后缀乘积
                suf = suf * grid[i][j] % MOD

        pre = 1  # 前缀乘积
        for i, row in enumerate(grid):
            for j, x in enumerate(row):
                p[i][j] = p[i][j] * pre % MOD  # 然后再乘上前缀乘积
                pre = pre * x % MOD

        return p