class Solution:
    def getCommon(self, nums1: List[int], nums2: List[int]) -> int:
        j, m = 0, len(nums2)
        for x in nums1:
            while j < m and nums2[j] < x:  # 找下一个 nums2[j] >= x
                j += 1
            if j < m and nums2[j] == x:
                return x
        return -1