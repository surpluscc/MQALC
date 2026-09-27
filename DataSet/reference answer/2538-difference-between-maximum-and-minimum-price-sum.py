class Solution:
    def maxOutput(self, n: int, edges: List[List[int]], price: List[int]) -> int:
        g = [[] for _ in range(n)]
        for x, y in edges:
            g[x].append(y)
            g[y].append(x)  # 建树

        ans = 0
        def dfs(x: int, fa: int) -> (int, int):
            nonlocal ans
            max_s1 = p = price[x]
            max_s2 = 0
            for y in g[x]:
                if y == fa: continue
                s1, s2 = dfs(y, x)
                # 前面最大带叶子的路径和 + 当前不带叶子的路径和
                # 前面最大不带叶子的路径和 + 当前带叶子的路径和
                ans = max(ans, max_s1 + s2, max_s2 + s1)
                max_s1 = max(max_s1, s1 + p)
                max_s2 = max(max_s2, s2 + p)  # 这里加上 p 是因为 x 必然不是叶子
            return max_s1, max_s2
        dfs(0, -1)
        return ans