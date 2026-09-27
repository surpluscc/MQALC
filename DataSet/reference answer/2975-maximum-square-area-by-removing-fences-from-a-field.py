class Solution:
    def maximizeSquareArea(self, m: int, n: int, hFences: List[int], vFences: List[int]) -> int:
        h = self.f(hFences, m)
        v = self.f(vFences, n)
        ans = max(h & v, default=0)
        return ans ** 2 % 1_000_000_007 if ans else -1

    def f(self, a: List[int], mx: int) -> Set[int]:
        a.extend([1, mx])
        a.sort()
        return set(y - x for x, y in combinations(a, 2))