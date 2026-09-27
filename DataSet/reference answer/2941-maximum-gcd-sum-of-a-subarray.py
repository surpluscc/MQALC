class Solution:
    def maxGcdSum(self, nums: List[int], k: int) -> int:

        ans = max(nums)**2 if k==1 else 0 #后面的代码对单个元素并没有更新答案，因此这里预处理这种情况
        g1 = {} # g1表示旧的gcd记录，g2表示新的gcd记录

        for num in nums:
            g2 = {num:(num,1)} # 注意1个元素当然也算子数组，不能漏掉
            for g in g1:
                gnew = math.gcd(g,num)
                if not (gnew in g2 and g2[gnew][0]>num+g1[g][0]): # 更新每个gcd的最大子数组和与最长子数组长度
                    g2[gnew]=(num+g1[g][0],g1[g][1]+1)    
                if g2[gnew][1]>=k and g2[gnew][0]*gnew>ans: # 更新答案，注意需要满足元素数量要求
                    ans = g2[gnew][0]*gnew
            g1 = g2
        
        return ans