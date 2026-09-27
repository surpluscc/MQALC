class Solution:
    def numberOfWays(self, n: int, m: int, k: int, source: List[int], dest: List[int]) -> int:

        mod = 10**9+7
        dp = [0,0,0,0]
        dp[(source[1]==dest[1])*2+(source[0]==dest[0])]=1 # 设边界条件
        
        for p in range(1,k+1):
            dp1 = [0,0,0,0] # 需要辅助数组，在一轮全部更新完之前不允许覆盖
            dp1[0] = (dp[0]*(n+m-4)+dp[1]*(n-1)+dp[2]*(m-1))%mod
            dp1[1] = (dp[0]+dp[1]*(m-2)+dp[3]*(m-1))%mod
            dp1[2] = (dp[0]+dp[2]*(n-2)+dp[3]*(n-1))%mod
            dp1[3] = (dp[1]+dp[2])%mod
            dp = dp1

        return dp[3] # 最终要的当然是x和y都正确