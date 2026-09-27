class Solution:
    def distance(self, nums: List[int]) -> List[int]:
        groups = defaultdict(list)
        for i, x in enumerate(nums):
            groups[x].append(i)  # 相同元素分到同一组，记录下标
        ans = [0] * len(nums)
        for a in groups.values():
            n = len(a)
            s = list(accumulate(a, initial=0))  # 前缀和
            for j, target in enumerate(a):
                left = target * j - s[j]  # 蓝色面积
                right = s[n] - s[j] - target * (n - j)  # 绿色面积
                ans[target] = left + right
        return ans