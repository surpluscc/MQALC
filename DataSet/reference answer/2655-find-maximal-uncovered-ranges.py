class Solution(object):
    def findMaximalUncoveredRanges(self, n, ranges):
        ranges.sort()
        res, c = [], 0
        for left, r in ranges:
            if c<left:
                res.append([c, left-1])
            if (t:=r+1)>c:c=t
        return res+[[c, n-1]] if c<n else res