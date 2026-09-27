class Solution:
    def maxProfit(self, prices: List[int], profits: List[int]) -> int:
        m=max(prices)
        n=len(prices)
        tree=[0]*(m+2)
        def update(x,val):
            while x<=m+1:
                tree[x]=max(tree[x],val)
                x+=x&(-x)
            return 
        def query(x):
            res=0
            while x>0:
                res=max(tree[x],res)
                x-=x&(-x)
            return res
        resleft,resright=[0]*n,[0]*n
        for i,k in enumerate(prices):#更新左边满足条件最大值
            resleft[i]=query(k)
            update(k+1,profits[i])
        tree=[0]*(m+2)
        for i in range(n-1,-1,-1):#更新右边满足条件最大值
            resright[i]=query(m-prices[i])
            update(m-prices[i]+1,profits[i])
        ans=-1
        for i in range(n):
            if resleft[i]>0 and resright[i]>0:
                ans=max(ans,resleft[i]+resright[i]+profits[i])
        return ans