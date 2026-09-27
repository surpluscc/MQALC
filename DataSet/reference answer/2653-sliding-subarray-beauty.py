class Solution:
    def getSubarrayBeauty(self, nums: List[int], k: int, x: int) -> List[int]:
        sl = SortedList(nums[:k - 1])  # SortedList 来自 sortedcontainers
        ans = []
        for in_, out in zip(nums[k - 1:], nums):
            sl.add(in_)  # 进入窗口（保证窗口有恰好 k 个数）
            ans.append(min(sl[x - 1], 0))
            sl.discard(out)  # 离开窗口（也可以写 remove）
        return ans