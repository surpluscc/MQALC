class Solution:
    def minFlips(self, grid: List[List[int]]) -> int:
        m, n = len(grid), len(grid[0])
        f = [float('inf')] * 4
        f[0] = 0
        for i in range((m + 1) // 2):
            for j in range((n + 1) // 2):
                ones = grid[i][j]
                cnt = 1
                if j != n - 1 - j:
                    ones += grid[i][n - 1 - j]
                    cnt += 1
                if i != m - 1 - i:
                    ones += grid[m - 1 - i][j]
                    cnt += 1
                if i != m - 1 - i and j != n - 1 - j:
                    ones += grid[m - 1 - i][n - 1 - j]
                    cnt += 1
                # 计算将这一组全部变为 1 的代价
                cnt1 = cnt - ones
                # 计算将这一组全部变为 0 的代价
                cnt0 = ones
                tmp = [0] * 4
                for k in range(4):
                    tmp[k] = f[k] + cnt0
                for k in range(4):
                    tmp[(k + cnt) % 4] = min(tmp[(k + cnt) % 4], f[k] + cnt1)
                f = tmp
        return f[0]