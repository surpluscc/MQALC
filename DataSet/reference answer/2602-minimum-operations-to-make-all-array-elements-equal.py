class Solution:
    def minOperations(self, nums: List[int], queries: List[int]) -> List[int]:
        n = len(nums)
        nums.sort()
        s = list(accumulate(nums, initial=0))  # 前缀和

        ans = []
        for q in queries:
            j = bisect_left(nums, q)
            left = q * j - s[j]  # 蓝色面积
            right = s[n] - s[j] - q * (n - j)  # 绿色面积
            ans.append(left + right)
        return ans