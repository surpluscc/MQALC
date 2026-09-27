class Solution:
    def maximumSetSize(self, nums1: List[int], nums2: List[int]) -> int:
        set1 = set(nums1)
        set2 = set(nums2)
        n = len(nums1)
        c1 = min(len(set1), n // 2)
        c2 = min(len(set2), n // 2)
        return min(len(set1 | set2), c1 + c2)