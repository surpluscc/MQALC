from sortedcontainers import SortedList

class Solution:
    def minAbsoluteDifference(self, nums: List[int], x: int) -> int:
        ans = inf
        sl = SortedList((-inf, inf))  # 哨兵
        for v, y in zip(nums, nums[x:]):
            sl.add(v)
            j = sl.bisect_left(y)
            ans = min(ans, sl[j] - y, y - sl[j - 1])
        return ans