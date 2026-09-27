
class Solution:
    def maxScore(self, prices: List[int]) -> int:
        dc = Counter()
        for i,v in enumerate(prices): dc[v-i] += v
        return max(dc.values())