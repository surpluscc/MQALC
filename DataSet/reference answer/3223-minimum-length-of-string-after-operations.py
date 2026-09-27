class Solution:
    def minimumLength(self, s: str) -> int:
        return sum((c - 1) % 2 + 1 for c in Counter(s).values())