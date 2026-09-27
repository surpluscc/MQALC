class Solution:
    def resultGrid(self, a: List[List[int]], threshold: int) -> List[List[int]]:
        m, n = len(a), len(a[0])
        result = [[0] * n for _ in range(m)]
        cnt = [[0] * n for _ in range(m)]
        for i in range(2, m):
            for j in range(2, n):
                # 检查左右相邻格子
                ok = True
                for row in a[i - 2: i + 1]:
                    if abs(row[j - 2] - row[j - 1]) > threshold or abs(row[j - 1] - row[j]) > threshold:
                        ok = False
                        break  # 不合法，下一个
                if not ok: continue

                # 检查上下相邻格子
                for y in range(j - 2, j + 1):
                    if abs(a[i - 2][y] - a[i - 1][y]) > threshold or abs(a[i - 1][y] - a[i][y]) > threshold:
                        ok = False
                        break  # 不合法，下一个
                if not ok: continue

                # 合法，计算 3x3 子网格的平均值
                avg = sum(a[x][y] for x in range(i - 2, i + 1) for y in range(j - 2, j + 1)) // 9

                # 更新 3x3 子网格内的 result
                for x in range(i - 2, i + 1):
                    for y in range(j - 2, j + 1):
                        result[x][y] += avg  # 先累加，最后再求平均值
                        cnt[x][y] += 1

        for i, row in enumerate(cnt):
            for j, c in enumerate(row):
                if c == 0:  # (i,j) 不属于任何子网格
                    result[i][j] = a[i][j]
                else:
                    result[i][j] //= c  # 求平均值
        return result