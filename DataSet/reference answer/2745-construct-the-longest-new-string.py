class Solution:
    def longestString(self, x: int, y: int, z: int) -> int:
        return (min(x, y) * 2 + (x != y) + z) * 2