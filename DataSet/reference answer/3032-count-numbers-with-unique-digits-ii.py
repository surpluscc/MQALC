class Solution:
    def numberCount(self, a: int, b: int) -> int:
        ans = 0
        for i in range(a,b+1):
            if len(str(i)) == len(set(str(i))):
                ans += 1
        return ans