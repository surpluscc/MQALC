class Solution:
    def countKSubsequencesWithMaxBeauty(self, s: str, k: int) -> int:
        MOD = 10 ** 9 + 7
        ans = 1
        cnt = Counter(Counter(s).values())
        for c, num in sorted(cnt.items(), reverse=True):
            if num >= k:
                return ans * pow(c, k, MOD) * comb(num, k) % MOD
            ans *= pow(c, num, MOD)
            k -= num
        return 0  # k 太大，无法选 k 个不一样的字符