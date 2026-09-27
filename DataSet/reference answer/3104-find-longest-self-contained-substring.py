class Solution:
    def maxSubstringLength(self, s: str) -> int:
        dc, res = {}, -1
        for i,v in enumerate(s):
            if v not in dc: dc[v] = [i,i,1]
            else:
                dc[v][1] = i
                dc[v][2] += 1
        lis, m = sorted(dc, key = lambda x:dc[x][0]), len(dc)
        for i in range(m):
            a, b, c = dc[lis[i]][0], 0, 0
            for j in range(i, m - (i == 0)):
                _, nb, nc = dc[lis[j]]
                b, c = max(b, nb), c + nc
                if b - a + 1 == c: res = max(res, c)
        return res
