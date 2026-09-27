class Solution:
    def maxPalindromesAfterOperations(self, words: List[str]) -> int:
        ans = tot = 0
        cnt = Counter()
        for w in words:
            tot += len(w)
            cnt += Counter(w)
        tot -= sum(c % 2 for c in cnt.values())  # 减去出现次数为奇数的字母

        words.sort(key=len)  # 按照长度从小到大排序
        for w in words:
            tot -= len(w) // 2 * 2  # 长为奇数的字符串，长度要减一
            if tot < 0: break
            ans += 1
        return ans