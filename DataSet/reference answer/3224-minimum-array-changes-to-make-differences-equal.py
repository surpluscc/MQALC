class Solution:
    def minChanges(self, nums: List[int], k: int) -> int:
        cnt = [0] * (k + 1)
        cnt2 = [0] * (k + 1)
        n = len(nums)
        for i in range(n // 2):
            p, q = nums[i], nums[n - 1 - i]
            if p > q:  # 保证 p <= q
                p, q = q, p
            cnt[q - p] += 1
            cnt2[max(q, k - p)] += 1

        ans = n
        sum2 = 0  # 统计有多少对 (p,q) 都要改
        for c, c2 in zip(cnt, cnt2):
            # 其他 n/2-c 对 (p,q) 至少要改一个数，在此基础上，有额外的 sum2 对 (p,q) 还要再改一个数
            ans = min(ans, n // 2 - c + sum2)
            # 对于后面的更大的 x，当前的这 c2 对 (p,q) 都要改
            sum2 += c2
        return ans