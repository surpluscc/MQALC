class Solution:
    def maximizeSquareHoleArea(self, n: int, m: int, hBars: List[int], vBars: List[int]) -> int:
        def f(a: List[int]) -> int:
            a.sort()
            n = len(a)
            mx = i = 0
            while i < n:
                st = i
                i += 1
                while i < n and a[i] - a[i - 1] == 1:
                    i += 1
                mx = max(mx, i - st)
            return mx + 1
        return min(f(hBars), f(vBars)) ** 2