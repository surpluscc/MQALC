# 由于乘法超过 64 位整数范围，需要用到 bigint，所以效率不如写法一
class Solution:
    def minimumCost(self, target: str, words: List[str], costs: List[int]) -> int:
        n = len(target)

        # 多项式字符串哈希（方便计算子串哈希值）
        # 哈希函数 hash(s) = s[0] * BASE^(n-1) + s[1] * BASE^(n-2) + ... + s[n-2] * BASE + s[n-1]
        MOD = 10 ** 18 + 3
        BASE = randint(8 * 10 ** 17, 9 * 10 ** 17)  # 随机 BASE，防止 hack
        pow_base = [1] + [0] * n  # pow_base[i] = BASE^i
        pre_hash = [0] * (n + 1)  # 前缀哈希值 pre_hash[i] = hash(s[:i])
        for i, b in enumerate(target):
            pow_base[i + 1] = pow_base[i] * BASE % MOD
            pre_hash[i + 1] = (pre_hash[i] * BASE + ord(b)) % MOD  # 秦九韶算法计算多项式哈希

        # 每个 words[i] 的哈希值 -> 最小成本
        min_cost = defaultdict(lambda: inf)
        for w, c in zip(words, costs):
            h = 0
            for b in w:
                h = (h * BASE + ord(b)) % MOD
            min_cost[h] = min(min_cost[h], c)

        # 有 O(√L) 个不同的长度
        sorted_lens = sorted(set(map(len, words)))

        f = [0] + [inf] * n
        for i in range(1, n + 1):
            for sz in sorted_lens:
                if sz > i:
                    break
                # 计算子串 target[i-sz:i] 的哈希值（计算方法类似前缀和）
                sub_hash = (pre_hash[i] - pre_hash[i - sz] * pow_base[sz]) % MOD
                # 手写 min，避免超时
                tmp = f[i - sz] + min_cost[sub_hash]
                if tmp < f[i]:
                    f[i] = tmp
        return -1 if f[n] == inf else f[n]