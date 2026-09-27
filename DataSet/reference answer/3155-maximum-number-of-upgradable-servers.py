class Solution:
    def maxUpgrades(self, count: List[int], upgrade: List[int], sell: List[int], money: List[int]) -> List[int]:
        n = len(count)
        ans = []
        for i in range(n):
            low = 0
            high = count[i]
            while low <= high:
                mid = (low + high) // 2
                if money[i] + (count[i] - mid) * sell[i] - (mid * upgrade[i]) < 0:
                    high = mid - 1
                else:
                    low = mid + 1
            
            ans.append(low - 1)
        
        return ans