class Solution:
    def maxHammingDistances(self, nums: List[int], m: int) -> List[int]:
        dp = []
        has = [float("inf")] * (1 << m)
        for i in nums:
            if has[i]:
                dp.append([0,i])
                has[i] = 0
        while dp:
            y, x = heapq.heappop(dp)
            if has[x] == y:
                y += 1
                for i in range(m):
                    nx = x ^ (1<<i)
                    if has[nx] > y:
                        has[nx] = y
                        heapq.heappush(dp, [y,nx])
        return [m-has[(-1)^i] for i in nums]