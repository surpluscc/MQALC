class Solution:
    def minimumSum(self, nums: List[int]) -> int:
        n = len(nums)
        suf = [0] * n
        suf[-1] = nums[-1]  # 后缀最小值
        for i in range(n - 2, 1, -1):
            suf[i] = min(suf[i + 1], nums[i])

        ans = inf
        pre = nums[0]  # 前缀最小值
        for j in range(1, n - 1):
            if pre < nums[j] > suf[j + 1]:  # 山形
                ans = min(ans, pre + nums[j] + suf[j + 1])  # 更新答案
            pre = min(pre, nums[j])
        return ans if ans < inf else -1