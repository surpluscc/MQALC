class Solution:
    def unmarkedSumArray(self, nums: List[int], queries: List[List[int]]) -> List[int]:
        n = len(nums)
        s = sum(nums)
        ids = sorted(range(n), key=lambda i: nums[i])  # 稳定排序
        ans = []
        j = 0
        for i, k in queries:
            s -= nums[i]
            nums[i] = 0  # 标记
            while j < n and k:
                i = ids[j]
                if nums[i]:  # 没有被标记
                    s -= nums[i]
                    nums[i] = 0
                    k -= 1
                j += 1
            ans.append(s)
        return ans