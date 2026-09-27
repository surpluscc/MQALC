class Solution:
    def minimumScore(self, s: str, t: str) -> int:
        n, m = len(s), len(t)
        suf = [m] * (n + 1)
        j = m - 1
        for i in range(n - 1, -1, -1):
            if s[i] == t[j]:
                j -= 1
            if j < 0:  # t 是 s 的子序列
                return 0
            suf[i] = j + 1

        ans = suf[0]  # 删除 t[:suf[0]]
        j = 0
        for i, c in enumerate(s):
            if c == t[j]:  # 注意上面判断了 t 是 s 子序列的情况，这里 j 不会越界
                j += 1
                ans = min(ans, suf[i + 1] - j)  # 删除 t[j:suf[i+1]]
        return ans