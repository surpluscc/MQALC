class Solution:
    def minEdgeReversals(self, n: int, edges: List[List[int]]) -> List[int]:
        g = [[] for _ in range(n)]
        for x, y in edges:
            g[x].append((y, 1))
            g[y].append((x, -1))  # 从 y 到 x 需要反向

        ans = [0] * n
        def dfs(x: int, fa: int) -> None:
            for y, dir in g[x]:
                if y != fa:
                    ans[0] += dir < 0
                    dfs(y, x)
        dfs(0, -1)

        def reroot(x: int, fa: int) -> None:
            for y, dir in g[x]:
                if y != fa:
                    ans[y] = ans[x] + dir  # dir 就是从 x 换到 y 的「变化量」
                    reroot(y, x)
        reroot(0, -1)
        return ans