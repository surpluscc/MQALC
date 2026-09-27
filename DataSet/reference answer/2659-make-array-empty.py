class Solution:
    def countOperationsToEmptyArray(self, nums: List[int]) -> int:
        ans = n = len(nums)
        id = sorted(range(n), key=lambda x: nums[x])
        for k, (pre, i) in enumerate(pairwise(id), 1):
            if i < pre:  # 必须多走一整圈
                ans += n - k  # 减去前面删除的元素个数
        return ans