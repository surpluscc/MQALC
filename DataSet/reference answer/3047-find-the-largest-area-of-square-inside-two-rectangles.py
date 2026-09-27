class Solution:
    def largestSquareArea(self, bottomLeft: List[List[int]], topRight: List[List[int]]) -> int:
        ans = 0
        for ((x1, y1), (x2, y2)), ((x3, y3), (x4, y4)) in combinations(zip(bottomLeft, topRight), 2):
            width = min(x2, x4) - max(x1, x3)  # 注：改成用 if-else 计算 min 和 max 会更快
            height = min(y2, y4) - max(y1, y3)
            size = min(width, height)
            if size > 0:
                ans = max(ans, size * size)
        return ans