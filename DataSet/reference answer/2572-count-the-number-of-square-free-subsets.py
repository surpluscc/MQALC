PRIMES = 2, 3, 5, 7, 11, 13, 17, 19, 23, 29
SF_TO_MASK = [0] * 31  # SF_TO_MASK[i] 为 i 的质因子集合（用二进制表示）
for i in range(2, 31):
    for j, p in enumerate(PRIMES):
        if i % p == 0:
            if i % (p * p) == 0:  # 有平方因子
                SF_TO_MASK[i] = -1
                break
            SF_TO_MASK[i] |= 1 << j  # 把 j 加到集合中

class Solution:
    def squareFreeSubsets(self, nums: List[int]) -> int:
        MOD = 10 ** 9 + 7
        M = 1 << len(PRIMES)
        f = [0] * M  # f[j] 表示恰好组成质数集合 j 的方案数
        f[0] = 1  # 质数集合是空集的方案数为 1
        for x in nums:
            mask = SF_TO_MASK[x]
            if mask >= 0:  # x 是 SF
                for j in range(M - 1, mask - 1, -1):
                    if (j | mask) == j:  # mask 是 j 的子集
                        f[j] = (f[j] + f[j ^ mask]) % MOD  # 不选 mask + 选 mask
        return (sum(f) - 1) % MOD  # -1 去掉空集（nums 的空子集）