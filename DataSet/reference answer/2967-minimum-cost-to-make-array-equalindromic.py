# 严格按顺序从小到大生成所有回文数（不用字符串转换）
pal = []
base = 1
while base <= 10000:
    # 生成奇数长度回文数
    for i in range(base, base * 10):
        x = i
        t = i // 10
        while t:
            x = x * 10 + t % 10
            t //= 10
        pal.append(x)
    # 生成偶数长度回文数
    if base <= 1000:
        for i in range(base, base * 10):
            x = t = i
            while t:
                x = x * 10 + t % 10
                t //= 10
            pal.append(x)
    base *= 10
pal.append(1_000_000_001)  # 哨兵，防止下面代码中的 i 下标越界

class Solution:
    def minimumCost(self, nums: List[int]) -> int:
        # 注：排序只是为了找中位数，如果用快速选择算法，可以做到 O(n)
        nums.sort()

        # 返回 nums 中的所有数变成 pal[i] 的总代价
        def cost(i: int) -> int:
            target = pal[i]
            return sum(abs(x - target) for x in nums)

        n = len(nums)
        i = bisect_left(pal, nums[(n - 1) // 2])  # 二分找中位数右侧最近的回文数
        if pal[i] <= nums[n // 2]:  # 回文数在中位数范围内
            return cost(i)  # 直接变成 pal[i]
        return min(cost(i - 1), cost(i))  # 枚举离中位数最近的两个回文数 pal[i-1] 和 pal[i]