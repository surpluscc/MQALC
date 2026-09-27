class Solution:
    def minimumTime(self, grid: List[List[int]]) -> int:
        m, n = len(grid), len(grid[0])
        if grid[0][1] > 1 and grid[1][0] > 1:  # 无法「等待」
            return -1

        dis = [[inf] * n for _ in range(m)]
        dis[0][0] = 0
        h = [(0, 0, 0)]
        while True:  # 可以等待，就一定可以到达终点
            d, i, j = heappop(h)
            if d > dis[i][j]: continue
            if i == m - 1 and j == n - 1:  # 找到终点，此时 d 一定是最短路
                return d
            for x, y in (i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1):  # 枚举周围四个格子
                if 0 <= x < m and 0 <= y < n:
                    nd = max(d + 1, grid[x][y])
                    nd += (nd - x - y) % 2  # nd 必须和 x+y 同奇偶
                    if nd < dis[x][y]:
                        dis[x][y] = nd  # 更新最短路
                        heappush(h, (nd, x, y))