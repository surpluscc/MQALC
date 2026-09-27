from sortedcontainers import SortedList

mod = 10**9+7
fact = [1]*100001
for p in range(2,100001):
    fact[p]=fact[p-1]*p%mod #用 n!= n * (n-1)!来预处理

class Solution:
    def getPermutationIndex(self, perm: List[int]) -> int:

        n = len(perm)
        lft = SortedList(range(1,n+1))
        ans = 0
        for p in range(n):
            ans=(ans+lft.bisect_left(perm[p])*fact[n-1-p])%mod
            lft.remove(perm[p]) # 关心的是多少更小的元素还没见过，因此见过就删了
        return ans
