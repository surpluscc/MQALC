class Solution:
    def sumOfEncryptedInt(self, nums: List[int]) -> int:
        ans = 0
        for x in nums:
            mx = base = 0
            while x:
                x, d = divmod(x, 10)
                mx = max(mx, d)
                base = base * 10 + 1
            ans += mx * base
        return ans