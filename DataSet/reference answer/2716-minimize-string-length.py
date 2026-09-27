class Solution:
    def minimizedStringLength(self, s: str) -> int:
        mask = 0
        for c in s:
            mask |= 1 << (ord(c) - ord('a'))
        return bin(mask).count('1')