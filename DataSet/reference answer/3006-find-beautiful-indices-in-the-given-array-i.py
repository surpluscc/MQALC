class Solution:
    def beautifulIndices(self, s: str, a: str, b: str, k: int) -> List[int]:
        pos_a = self.kmp(s, a)
        pos_b = self.kmp(s, b)

        ans = []
        j, m = 0, len(pos_b)
        for i in pos_a:
            while j < m and pos_b[j] < i - k:
                j += 1
            if j < m and abs(pos_b[j] - i) <= k:
                ans.append(i)
        return ans

    def kmp(self, text: str, pattern: str) -> List[int]:
        m = len(pattern)
        pi = [0] * m
        c = 0
        for i in range(1, m):
            v = pattern[i]
            while c and pattern[c] != v:
                c = pi[c - 1]
            if pattern[c] == v:
                c += 1
            pi[i] = c

        res = []
        c = 0
        for i, v in enumerate(text):
            v = text[i]
            while c and pattern[c] != v:
                c = pi[c - 1]
            if pattern[c] == v:
                c += 1
            if c == len(pattern):
                res.append(i - m + 1)
                c = pi[c - 1]
        return res