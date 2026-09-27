class Solution:
    def removeAlmostEqualCharacters(self, s: str) -> int:
        ans = 0
        i, n = 1, len(s)
        while i < n:
            if abs(ord(s[i - 1]) - ord(s[i])) <= 1:
                ans += 1
                i += 2
            else:
                i += 1
        return ans