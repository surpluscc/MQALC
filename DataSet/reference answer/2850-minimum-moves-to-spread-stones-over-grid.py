class Solution:
    def minimumMoves(self, grid: List[List[int]]) -> int:
        # itertools.permutations 无法对生成的全排列去重
        def my_permutations(x: List[Any]) -> List[Any]:
            n = len(x)
            while True:
                yield x
                # 生成下一个排列
                p = -1
                for i in range(n - 1):
                    if x[i] < x[i + 1]:
                        p = i
                if p == -1:
                    return
                q = -1
                for j in range(p + 1, n):
                    if x[p] < x[j]:
                        q = j
                x[p], x[q] = x[q], x[p]
                i, j = p + 1, n - 1
                while i < j:
                    x[i], x[j] = x[j], x[i]
                    i += 1
                    j -= 1

        more, less = list(), list()
        for i in range(3):
            for j in range(3):
                if grid[i][j] > 1:
                    more.extend([(i, j)] * (grid[i][j] - 1))
                elif grid[i][j] == 0:
                    less.append((i, j))

        ans = inf
        total = 0
        for perm in my_permutations(more):
            steps = 0
            for (px, py), (lx, ly) in zip(perm, less):
                total += 1
                steps += abs(px - lx) + abs(py - ly)
            ans = min(ans, steps)
        return ans