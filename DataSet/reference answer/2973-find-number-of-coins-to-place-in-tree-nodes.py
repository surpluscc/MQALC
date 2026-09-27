class Solution:
    def placedCoins(self, edges: List[List[int]], cost: List[int]) -> List[int]:
        n = len(cost)
        g = [[] for _ in range(n)]
        for x, y in edges:
            g[x].append(y)
            g[y].append(x)

        ans = [1] * n
        def dfs(x: int, fa: int) -> List[int]:
            a = [cost[x]]
            for y in g[x]:
                if y != fa:
                    a.extend(dfs(y, x))
            a.sort()
            m = len(a)
            if m >= 3:
                ans[x] = max(a[-3] * a[-2] * a[-1], a[0] * a[1] * a[-1], 0)
            if m > 5:
                a = a[:2] + a[-3:]
            return a
        dfs(0, -1)
        return ans