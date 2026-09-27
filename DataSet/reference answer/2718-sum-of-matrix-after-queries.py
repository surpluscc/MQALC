class Solution:
    def matrixSumQueries(self, n: int, queries: List[List[int]]) -> int:
        ans = 0
        vis = [set(), set()]
        for type, index, val in reversed(queries):
            if index not in vis[type]:  # 后面（>i）没有对这一行/列的操作
                # 这一行/列还剩下 n-len(vis[type^1]) 个可以填入的格子
                ans += (n - len(vis[type ^ 1])) * val
                vis[type].add(index)  # 标记操作过
        return ans