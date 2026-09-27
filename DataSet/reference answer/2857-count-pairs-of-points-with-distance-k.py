class Solution:
    def countPairs(self, coordinates: List[List[int]], k: int) -> int:
        ans = 0
        cnt = Counter()
        for x, y in coordinates:
            for i in range(k + 1):
                ans += cnt[x ^ i, y ^ (k - i)]  # tuple 的括号可以省略
            cnt[x, y] += 1  # tuple 的括号可以省略
        return ans