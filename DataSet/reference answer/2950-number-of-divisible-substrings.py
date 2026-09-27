class Solution:
    def countDivisibleSubstrings(self, word: str) -> int:
        r = 0
        for i in range(1, 10):
            have = {0: 1}
            s = 0
            for c in word:
                s += 9 - (ord('z') - ord(c)) // 3 - i
                r += have.get(s, 0)
                have[s] = have.get(s, 0) + 1
        return r
        