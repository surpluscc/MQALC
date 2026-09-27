class Solution:
    def lastNonEmptyString(self, s: str) -> str:
        last = {c: i for i, c in enumerate(s)}
        cnt = Counter(s)
        mx = max(cnt.values())
        ids = sorted(last[ch] for ch, c in cnt.items() if c == mx)
        return ''.join(s[i] for i in ids)