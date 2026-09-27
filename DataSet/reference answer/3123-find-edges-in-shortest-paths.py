class Solution:
    def findAnswer(self, n: int, edges: List[List[int]]) -> List[bool]:
        g = [[] for _ in range(n)]
        for i, (x, y, w) in enumerate(edges):
            g[x].append((y, w, i))
            g[y].append((x, w, i))

        # Dijkstra 算法模板
        dis = [inf] * n
        dis[0] = 0
        h = [(0, 0)]
        while h:
            dx, x = heappop(h)
            if dx > dis[x]:
                continue
            for y, w, _ in g[x]:
                new_dis = dx + w
                if new_dis < dis[y]:
                    dis[y] = new_dis
                    heappush(h, (new_dis, y))

        ans = [False] * len(edges)
        # 图不连通
        if dis[-1] == inf:
            return ans

        # 从终点出发 DFS
        vis = [False] * n
        def dfs(y: int) -> None:
            vis[y] = True
            for x, w, i in g[y]:
                if dis[x] + w != dis[y]:
                    continue
                ans[i] = True
                if not vis[x]:
                    dfs(x)
        dfs(n - 1)
        return ans