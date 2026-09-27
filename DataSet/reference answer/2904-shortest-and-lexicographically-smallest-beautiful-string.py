class Solution:
    def shortestBeautifulSubstring(self, s: str, k: int) -> str:
        # 1 的个数不足 k
        if s.count('1') < k:
            return ''
        # 否则一定有解
        for size in count(k):  # 从 k 开始枚举
            ans = ''
            for i in range(size, len(s) + 1):
                t = s[i - size: i]
                if (ans == '' or t < ans) and t.count('1') == k:
                    ans = t
            if ans: return ans