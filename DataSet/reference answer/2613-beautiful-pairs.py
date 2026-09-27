from sortedcontainers import SortedList

class Solution:
    def beautifulPair(self, nums1: List[int], nums2: List[int]) -> List[int]:
        n = len(nums1)
        ans = [n, n]
        h = {}
        a = []
        for i, (x, y) in enumerate(zip(nums1, nums2)):
            if (x, y) in h:
                i0, i1 = min(h[(x, y)], i), max(h[(x, y)], i)
                if i0 < ans[0] or i0 == ans[0] and i1 < ans[1]:
                    ans[0] = i0
                    ans[1] = i1
            else:
                h[(x, y)] = i
            a.append((x, y, i))
        
        if ans[0] < n and ans[1] < n:
            return ans
        
        a.sort()
        mn = n * 3
        s = SortedList(key=lambda x: x[1])
        l = 0
        for i in range(n):
            while l < i and a[i][0] - a[l][0] > mn:
                s.remove(a[l])
                l += 1
            idx = s.bisect_left((a[i][0], a[i][1] - mn, -1))
            while idx < len(s) and s[idx][1] - a[i][1] <= mn:
                d = abs(s[idx][0] - a[i][0]) + abs(s[idx][1] - a[i][1])
                i0, i1 = min(s[idx][2], a[i][2]), max(s[idx][2], a[i][2])
                if d < mn or d == mn and i0 < ans[0] or d == mn and i0 == ans[0] and i1 < ans[1]:
                    mn = d
                    ans[0] = i0
                    ans[1] = i1
                idx += 1
            s.add(a[i])
        return ans