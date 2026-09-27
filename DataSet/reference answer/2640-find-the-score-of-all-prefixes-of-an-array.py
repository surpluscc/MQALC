class Solution:
    def findPrefixScore(self, nums: List[int]) -> List[int]:
        ans = []
        mx = s = 0
        for x in nums:
            mx = max(mx, x)  # 前缀最大值
            s += x + mx  # 累加前缀的得分
            ans.append(s)
        return ans