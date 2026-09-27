class Solution:
    def findHighAccessEmployees(self, access_times: List[List[str]]) -> List[str]:
        name2times = defaultdict(list)
        for name, s in access_times:
            t = int(s[:2]) * 60 + int(s[2:])
            name2times[name].append(t)

        ans = []
        for name, a in name2times.items():
            a.sort()
            if any(a[i] - a[i - 2] < 60 for i in range(2, len(a))):
                ans.append(name)
        return ans