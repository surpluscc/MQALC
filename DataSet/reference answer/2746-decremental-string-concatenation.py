class Solution:
    def minimizeConcatenatedLength(self, words: List[str]) -> int:
        # 第 i 次操作，前面字符串开头为 s，末尾为e形成的最短长度        
        @cache
        def dfs(i: int, s: str, e: str) -> int:
            if i == n:
                return 0
            string = words[i]
            res = dfs(i + 1, s, string[-1]) + len(string) - int(string[0] == e)
            res = min(res, dfs(i + 1,string[0], e) + len(string) - int(string[-1] == s))
            return res
        n = len(words)
        return dfs(1, words[0][0], words[0][-1]) + len(words[0])