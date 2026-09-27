class Solution:
    def countCompleteSubstrings(self, word: str, k: int) -> int:
        def f(s: str) -> int:
            res = 0
            for m in range(1, 27):
                if k * m > len(s):
                    break
                cnt = Counter()
                for right, c in enumerate(s):
                    cnt[c] += 1
                    left = right + 1 - k * m
                    if left >= 0:
                        res += all(c == 0 or c == k for c in cnt.values())
                        cnt[s[left]] -= 1
            return res

        n = len(word)
        ans = i = 0
        while i < n:
            st = i
            i += 1
            while i < n and abs(ord(word[i]) - ord(word[i - 1])) <= 2:
                i += 1
            ans += f(word[st:i])
        return ans