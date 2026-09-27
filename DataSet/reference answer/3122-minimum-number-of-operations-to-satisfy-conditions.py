class Solution:
    def minimumOperations(self, grid: List[List[int]]) -> int:
        f0, f1, pre = 0, 0, -1
        for col in zip(*grid):
            mx, mx2, x = f0, 0, -1  # 不保留任何数字
            for v, c in Counter(col).items():
                res = (f0 if v != pre else f1) + c  # 保留元素 v
                if res > mx:  # 更新最优解和次优解
                    mx, mx2, x = res, mx, v
                elif res > mx2:  # 更新次优解
                    mx2 = res
            f0, f1, pre = mx, mx2, x
        return len(grid) * len(grid[0]) - f0