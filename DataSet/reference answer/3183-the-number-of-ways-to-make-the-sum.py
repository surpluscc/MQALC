class Solution:
    def numberOfWays(self, n: int) -> int:
        
        m = n//2-1
        correction = (m%3 == 0) + 1
        first, last, cnt = 3*m, (3*m)%9, m//3+1

        ans = (first + last) * cnt//2 + correction  # <-- the closed form

        return ans %1_000_000_007 