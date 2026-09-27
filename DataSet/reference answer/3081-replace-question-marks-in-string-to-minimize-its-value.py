class Solution:
    def minimizeStringValue(self, s: str) -> str:
        freq = [0] * 26
        for c in s:
            if c != '?':
                freq[ord(c) - ord('a')] += 1

        f = sorted(freq) + [inf]  # 哨兵
        q = s.count('?')
        for i in count(1):
            need = i * (f[i] - f[i - 1])
            if q <= need:
                limit, extra = f[i - 1] + q // i, q % i
                break
            q -= need

        target = freq.copy()
        for i in range(26):
            if target[i] > limit:
                continue
            target[i] = limit
            if extra:  # 还可以多分配一个
                extra -= 1
                target[i] += 1

        ans = list(s)
        j = 0
        for i, c in enumerate(ans):
            if c != '?':
                continue
            while freq[j] == target[j]:
                j += 1
            freq[j] += 1
            ans[i] = ascii_lowercase[j]
        return ''.join(ans)