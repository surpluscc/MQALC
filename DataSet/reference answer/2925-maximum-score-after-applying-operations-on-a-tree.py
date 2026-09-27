class Solution:
    def maximumScoreAfterOperations(self, edges: List[List[int]], values: List[int]) -> int:
        g = [[] for _ in values]
        g[0].append(-1)  # 避免误把根节点当作叶子
        for x, y in edges:
            g[x].append(y)
            g[y].append(x)

        # dfs(x, fa) 计算以 x 为根的子树是健康时，失去的最小分数
        def dfs(x: int, fa: int) -> int:
            if len(g[x]) == 1:  # x 是叶子
                return values[x]
            loss = 0  # 第二种情况
            for y in g[x]:
                if y != fa:
                    loss += dfs(y, x)  # 计算以 y 为根的子树是健康时，失去的最小分数
            return min(values[x], loss)  # 两种情况取最小值
        return sum(values) - dfs(0, -1)