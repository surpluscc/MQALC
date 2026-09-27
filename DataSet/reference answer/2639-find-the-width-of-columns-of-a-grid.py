class Solution:
    def findColumnWidth(self, grid: List[List[int]]) -> List[int]:
        n, m = len(grid), len(grid[0])
        res = [0] * m
        for i in range(n):
            for j in range(m):
                res[j] = max(res[j], len(str(grid[i][j])))
        return res