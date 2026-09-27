class Solution:
    def countTheNumOfKFreeSubsets(self, nums: List[int], k: int) -> int:

        nums.sort() #先对整个数组排序，这样每组就自然有序了
        grps = defaultdict(list) # Python也可二维列表，第一维长度为k，但用哈希表能适用值域和k很大的情形
        # mod = 10**9+7

        for num in nums: # 对k取模排序分组
            grps[num%k].append(num)

        ans = 1
        for grp in grps.values():
            dp = [0]*len(grp)
            dp[0]=2 #首项可以选或不选
            for j in range(1,len(grp)):
                if grp[j]-grp[j-1]==k:
                    dp[j]=dp[j-1]+dp[j-2] if j>1 else dp[j-1]+1 # 这时选当前项则不能选上一项，注意非法下标表示空集，方案数为1
                else:
                    dp[j]=2*dp[j-1] # 这时选不选当前项，上一项都能选
                # dp[j]%=mod
            ans*=dp[-1] #乘法原理
            # ans%=mod
        return ans