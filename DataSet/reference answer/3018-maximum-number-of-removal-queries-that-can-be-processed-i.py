class Solution:
    def maximumProcessableQueries(self, nums: List[int], queries: List[int]) -> int:
        n,m = len(nums),len(queries)        
        '''
        # 左右缩短至 l,r
        dp[l][r] 处理了 k 个值，l和r都还没用
        外向里dp
        ''' 
        # 左右加一位哨兵       
        dp = [[0] * (n+2) for _ in range(n+2)]
        # init
        dp[1][n] = 0        
        # l,r 长度
        for k in range(n,0,-1):
            # 起点
            for l in range(1,n-k+2):
                r = l + k - 1
                i = dp[l][r]
                # 以满足整个 queries
                if i == m:
                    return m
                                    
                # 移除左侧
                if nums[l-1] >= queries[i]:
                    if i + 1 > dp[l+1][r]:
                        dp[l+1][r] = i + 1
                elif i > dp[l+1][r]:
                    dp[l+1][r] = i
                # 移除右侧
                if nums[r-1] >= queries[i]:
                    if i + 1 > dp[l][r-1]:
                        dp[l][r-1] = i + 1
                elif i > dp[l][r-1]:
                    dp[l][r-1] = i
        # 获取结果
        res = 0
        for i in range(len(dp)):
            for j in range(len(dp[0])):
                if dp[i][j] > res:
                    res = dp[i][j]
                    
        return res