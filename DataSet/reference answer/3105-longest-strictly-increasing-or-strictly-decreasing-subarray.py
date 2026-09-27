class Solution:
    def longestMonotonicSubarray(self, a: List[int]) -> int:
        ans = 1
        i, n = 0, len(a)
        while i < n - 1:
            if a[i + 1] == a[i]:
                i += 1  # 直接跳过
                continue
            i0 = i  # 记录这一组的开始位置
            inc = a[i + 1] > a[i]  # 定下基调：是严格递增还是严格递减
            i += 2  # i 和 i+1 已经满足要求，从 i+2 开始判断
            while i < n and a[i] != a[i - 1] and (a[i] > a[i - 1]) == inc:
                i += 1
            # 从 i0 到 i-1 是满足题目要求的（并且无法再延长的）子数组
            ans = max(ans, i - i0)
            i -= 1
        return ans