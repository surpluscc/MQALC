class Solution:
    def minimumOperationsToWriteY(self, grid: List[List[int]]) -> int:
        cnt1 = [0] * 3
        cnt2 = [0] * 3
        n = len(grid)
        m = n // 2

        for i, row in enumerate(grid[:m]):
            cnt1[row[i]] += 1
            cnt1[row[-1 - i]] += 1
            for j, x in enumerate(row):
                if j != i and j != n - 1 - i:
                    cnt2[x] += 1
        for row in grid[m:]:
            cnt1[row[m]] += 1
            for j, x in enumerate(row):
                if j != m:
                    cnt2[x] += 1

        max_not_change = 0
        for i, c1 in enumerate(cnt1):
            for j, c2 in enumerate(cnt2):
                if i != j:
                    max_not_change = max(max_not_change, c1 + c2)
        return n * n - max_not_change