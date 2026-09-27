class Solution:
    def maxScore(self, nums1: List[int], nums2: List[int], k: int) -> int:
        a = sorted(zip(nums1, nums2), key=lambda p: -p[1])
        h = [x for x, _ in a[:k]]
        heapify(h)
        s = sum(h)
        ans = s * a[k - 1][1]
        for x, y in a[k:]:
            if x > h[0]:
                s += x - heapreplace(h, x)
                ans = max(ans, s * y)
        return ans