class Solution:
    def maximumLengthSubstring(self, s: str) -> int:
        ans = left = 0
        cnt = defaultdict(int)
        for i, c in enumerate(s):
            cnt[c] += 1
            while cnt[c] > 2:
                cnt[s[left]] -= 1
                left += 1
            ans = max(ans, i - left + 1)
        return ans