class Fenwick:
    __slots__ = 'f'

    def __init__(self, n: int):
        self.f = [0] * n

    def update(self, i: int, val: int) -> None:
        while i < len(self.f):
            self.f[i] += val
            i += i & -i

    def pre(self, i: int) -> int:
        res = 0
        while i > 0:
            res += self.f[i]
            i &= i - 1
        return res

    def query(self, l: int, r: int) -> int:
        if r < l:
            return 0
        return self.pre(r) - self.pre(l - 1)

class Solution:
    def countOfPeaks(self, nums, queries):
        n = len(nums)
        f = Fenwick(n - 1)
        def update(i: int, val: int) -> None:
            if nums[i - 1] < nums[i] and nums[i] > nums[i + 1]:
                f.update(i, val)
        for i in range(1, n - 1):
            update(i, 1)

        ans = []
        for op, i, val in queries:
            if op == 1:
                ans.append(f.query(i + 1, val - 1))
                continue
            for j in range(max(i - 1, 1), min(i + 2, n - 1)):
                update(j, -1)
            nums[i] = val
            for j in range(max(i - 1, 1), min(i + 2, n - 1)):
                update(j, 1)
        return ans