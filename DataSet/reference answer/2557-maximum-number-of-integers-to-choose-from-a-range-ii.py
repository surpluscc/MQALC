class Solution:
    def maxCount(self, banned: List[int], n: int, maxSum: int) -> int:

        ban = [0]+sorted(set(banned))+[n+1] #由于banned不保证有序且无重复，必须去重后排序
        ans = 0
        for j in range(1,len(ban)):
            first = ban[j-1]+1 
            cnt = ban[j]-ban[j-1]-1 #注意ban里的数值都是不能用的，首项和项数别搞错了
            sm = first*cnt+cnt*(cnt-1)//2 # 整个等差数列求和
            if sm<maxSum:
                maxSum-=sm
                ans+=cnt # 整个数列全取，继续遍历
            else:
                return ans+int(.5-first+(first*(first-1)+2*maxSum+.25+1e-10)**.5) #当前数列只能取一部分
        return ans