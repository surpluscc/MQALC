class Solution:
    def minOperations(self, nums1: List[int], nums2: List[int]) -> int:
        def f(last1: int, last2: int) -> int:
            res = 0
            for x, y in zip(nums1, nums2):
                if x > last1 or y > last2:
                    if y > last1 or x > last2:
                        return inf
                    res += 1
            return res
        ans = min(f(nums1[-1], nums2[-1]), f(nums2[-1], nums1[-1]))
        return ans if ans < inf else -1