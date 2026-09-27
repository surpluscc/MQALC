class Solution:
    def findKthSmallest(self, coins: List[int], k: int) -> int:
        coins.sort()
        a = []
        for x in coins:
            if all(x % y for y in a):
                a.append(x)

        subset_lcm = [1] * (1 << len(a))
        for i, x in enumerate(a):
            bit = 1 << i
            for mask in range(bit):
                # 刷表法 DP，在集合 mask 的基础上添加元素 i
                subset_lcm[bit | mask] = lcm(subset_lcm[mask], x)

        def check(m: int) -> bool:
            cnt = 0
            for i in range(1, len(subset_lcm)):  # 枚举所有非空子集
                cnt += m // subset_lcm[i] if i.bit_count() % 2 else -(m // subset_lcm[i])
            return cnt >= k
        return bisect_left(range(a[0] * k), True, k, key=check)