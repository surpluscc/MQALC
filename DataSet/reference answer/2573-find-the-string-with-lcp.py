class Solution:
    def findTheString(self, lcp: List[List[int]]) -> str:
        i, n = 0, len(lcp)
        s = [''] * n
        for c in ascii_lowercase:
            while i < n and s[i]: i += 1
            if i == n: break  # 构造完毕
            for j in range(i, n):
                if lcp[i][j]:
                    s[j] = c
        if '' in s: return ""  # 没有构造完

        # 直接在原数组上验证
        for i in range(n - 1, -1, -1):
            for j in range(n - 1, -1, -1):
                actual_lcp = 0 if s[i] != s[j] else 1 if i == n - 1 or j == n - 1 else lcp[i + 1][j + 1] + 1
                if lcp[i][j] != actual_lcp: return ""
        return "".join(s)