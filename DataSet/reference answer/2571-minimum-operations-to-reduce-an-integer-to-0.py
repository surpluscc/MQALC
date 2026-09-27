class Solution:
    def minOperations(self, n: int) -> int:
        return (3 * n ^ n).bit_count()