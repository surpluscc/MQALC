class Solution:
    def countSubmatrices(self, grid: List[List[int]], k: int) -> int:
        ans = 0
        col_sum = [0] * len(grid[0])
        for row in grid:
            s = 0
            for j, x in enumerate(row):
                col_sum[j] += x
                s += col_sum[j]
                if s > k:
                    break
                ans += 1
        return ans