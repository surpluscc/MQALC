class Solution:
    def maxCount(self, banned: List[int], n: int, maxSum: int) -> int:
        ans, s = 0, set(banned)
        for i in range(1, n + 1):
            if i > maxSum: break
            if i not in s:
                maxSum -= i
                ans += 1
        return ans