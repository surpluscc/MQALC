class Solution:
    def minimumPushes(self, word: str) -> int:
        a = sorted(Counter(word).values(), reverse=True)
        return sum(c * (i // 8 + 1) for i, c in enumerate(a))