class Solution:
    def countMatchingSubarrays(self, nums: List[int], pattern: List[int]) -> int:
        m = len(pattern)
        pattern.append(2)
        pattern.extend((y > x) - (y < x) for x, y in pairwise(nums))

        n = len(pattern)
        z = [0] * n
        l = r = 0
        for i in range(1, n):
            if i <= r:
                z[i] = min(z[i - l], r - i + 1)
            while i + z[i] < n and pattern[z[i]] == pattern[i + z[i]]:
                l, r = i, i + z[i]
                z[i] += 1

        return sum(lcp == m for lcp in z[m + 1:])