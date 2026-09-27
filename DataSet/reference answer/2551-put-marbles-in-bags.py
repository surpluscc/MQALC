class Solution:
    def putMarbles(self, weights: List[int], k: int) -> int:
        for i in range(len(weights) - 1):
            weights[i] += weights[i + 1]  # 原地求前缀和
        weights.pop()
        weights.sort()
        return sum(weights[len(weights) - k + 1:]) - sum(weights[:k - 1])