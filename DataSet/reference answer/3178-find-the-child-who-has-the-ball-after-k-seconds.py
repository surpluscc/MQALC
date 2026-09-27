class Solution:
    def numberOfChild(self, n: int, k: int) -> int:
        k, t = divmod(k, n - 1)
        return n - t - 1 if k % 2 else t