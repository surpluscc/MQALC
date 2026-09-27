class Solution:
    def countSubMultisets(self, nums: List[int], l: int, r: int) -> int:
        MOD = 10 ** 9 + 7
        total = sum(nums)
        if l > total:
            return 0

        r = min(r, total)
        cnt = Counter(nums)
        f = [cnt[0] + 1] + [0] * r
        del cnt[0]

        s = 0
        for x, c in cnt.items():
            s = min(s + x * c, r)
            for j in range(x, s + 1):
                f[j] = (f[j] + f[j - x]) % MOD  # 原地计算同余前缀和
            t = (c + 1) * x
            for j in range(s, t - 1, -1):
                f[j] = (f[j] - f[j - t]) % MOD  # 两个同余前缀和的差
        return sum(f[l:]) % MOD