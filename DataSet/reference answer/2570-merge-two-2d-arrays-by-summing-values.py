class Solution:
    def mergeArrays(self, a: List[List[int]], b: List[List[int]]) -> List[List[int]]:
        ans = []
        i, n = 0, len(a)
        j, m = 0, len(b)
        while True:
            if i == n:
                ans.extend(b[j:])
                return ans
            if j == m:
                ans.extend(a[i:])
                return ans
            if a[i][0] < b[j][0]:
                ans.append(a[i])
                i += 1
            elif a[i][0] > b[j][0]:
                ans.append(b[j])
                j += 1
            else:
                a[i][1] += b[j][1]
                ans.append(a[i])
                i += 1
                j += 1