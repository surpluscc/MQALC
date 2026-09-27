class Solution:
    def minimumPushes(self, word: str) -> int:
        k, rem = divmod(len(word), 8)
        return (k * 4 + rem) * (k + 1)