# 预处理 2**15 以内的 5 的幂
pow5 = [bin(5 ** i)[2:] for i in range(7)]

class Solution:
    def minimumBeautifulSubstrings(self, s: str) -> int:
        n = len(s)
        @cache
        def dfs(i: int) -> int:
            if i == n: return 0
            if s[i] == '0': return inf  # 不能包含前导 0
            res = inf
            for t in pow5:
                if i + len(t) > n:
                    break
                if s[i: i + len(t)] == t:  # 忽略切片的时间，这里的比较视作均摊 O(1)
                    res = min(res, dfs(i + len(t)) + 1)
            return res
        ans = dfs(0)
        return ans if ans < inf else -1