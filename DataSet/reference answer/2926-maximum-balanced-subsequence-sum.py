class Solution:
    def maxBalancedSubsequenceSum(self, nums: List[int]) -> int:
        b = sorted(set(x - i for i, x in enumerate(nums)))  # 离散化 nums[i]-i
        t = BIT(len(b) + 1)
        for i, x in enumerate(nums):
            j = bisect_left(b, x - i) + 1  # nums[i]-i 离散化后的值（从 1 开始）
            f = max(t.pre_max(j), 0) + x
            t.update(j, f)
        return t.pre_max(len(b))  # 所有 f 的最大值

# 树状数组模板（维护前缀最大值）
class BIT:
    def __init__(self, n: int):
        self.tree = [-inf] * n

    def update(self, i: int, val: int) -> None:
        while i < len(self.tree):
            self.tree[i] = max(self.tree[i], val)
            i += i & -i

    def pre_max(self, i: int) -> int:
        mx = -inf
        while i > 0:
            mx = max(mx, self.tree[i])
            i &= i - 1
        return mx