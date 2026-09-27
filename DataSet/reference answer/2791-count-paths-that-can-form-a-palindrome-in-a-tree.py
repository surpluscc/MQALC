class Solution:
    def countPalindromePaths(self, parent: List[int], s: str) -> int:
        n = len(s)
        g = [[] for _ in range(n)]
        for i in range(1, n):
            g[parent[i]].append(i)

        cnt = Counter([0])  # 一条「空路径」
        def dfs(v: int, xor: int) -> int:
            res = 0
            for w in g[v]:
                bit = 1 << (ord(s[w]) - ord('a'))
                x = xor ^ bit
                res += cnt[x] + sum(cnt[x ^ (1 << i)] for i in range(26))
                cnt[x] += 1
                res += dfs(w, x)
            return res
        return dfs(0, 0)