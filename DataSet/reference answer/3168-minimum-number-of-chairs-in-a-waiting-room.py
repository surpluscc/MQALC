class Solution:
    def minimumChairs(self, s: str) -> int:
        ans = cnt = 0
        for c in s:
            if c == 'E':
                cnt += 1
                ans = max(ans, cnt)
            else:
                cnt -= 1
        return ans