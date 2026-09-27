class Solution:
    def numberOfSubmatrices(self, grid: List[List[str]]) -> int:
        ans = 0
        col_cnt = [[0, 0] for _ in grid[0]]
        for row in grid:
            s0 = s1 = 0
            for j, c in enumerate(row):
                if c != '.':
                    col_cnt[j][ord(c) & 1] += 1
                s0 += col_cnt[j][0]
                s1 += col_cnt[j][1]
                if s0 and s0 == s1:
                    ans += 1
        return ans