class Solution:
    def numberOfSpecialChars(self, word: str) -> int:
        mask = [0, 0]
        for c in map(ord, word):
            mask[c >> 5 & 1] |= 1 << (c & 31)
        return (mask[0] & mask[1]).bit_count()