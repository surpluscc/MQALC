class Solution:
    def maxKelements(self, nums: List[int], k: int) -> int:
        # python 中的 heap 默认是小根堆，需要对元素取相反数
        q = [-x for x in nums]
        heapify(q)

        ans = 0
        for _ in range(k):
            x = heappop(q)
            ans += -x
            heappush(q, -((-x + 2) // 3))
        return ans