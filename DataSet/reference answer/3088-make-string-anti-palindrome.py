class Solution:
    def makeAntiPalindrome(self, s: str) -> str:
        cnt = Counter(s)
        n = len(s)
        for c in cnt.keys():
            if cnt[c] > n // 2:#如果超过一半就是-1
                return str(-1)
        ans = []
        for c in sorted(cnt.keys()):
            ans += [c] * cnt[c]
        if ans[n // 2 - 1] == ans[n // 2]:#如果中间相等需要换位置
            r, s = 0, 1
            while ans[n // 2 - 1 - r] == ans[n // 2 + r] or (n // 2 + r + 1 < n and ans[n // 2 - 1] == ans[n // 2 + r]):#计算出需要换位置的长度
                r += 1
            while ans[n // 2] == ans[n // 2 - 1 - s]:#需要换多远
                s += 1
            sb = ans[n // 2 : n // 2 + r]
            ans[n // 2 : n // 2 + r] = []#清空这一段
            for i in range(len(sb)):
                ans.insert(n // 2 + s + i, sb[i])#依次插入
        return "".join(ans)