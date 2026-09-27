class Solution:
    def minOperations(self, nums1: List[int], nums2: List[int], k: int) -> int:
        ans = sum = 0
        for x, y in zip(nums1, nums2):
            x -= y
            if k:
                if x % k: return -1
                sum += x // k
                if x > 0: ans += x // k
            elif x: return -1
        return -1 if sum else ans