class Solution:
    def countOfPairs(self, n: int, x: int, y: int) -> List[int]:
        if x > y:
            x, y = y, x

        if x + 1 >= y:
            return list(range((n - 1) * 2, -1, -2))

        diff = [0] * (n + 1)

        def add(l: int, r: int) -> None:
            diff[l] += 2
            diff[r + 1] -= 2

        for i in range(1, n):
            if i <= x:
                k = (x + y + 1) // 2
                add(1, k - i)
                add(x - i + 2, x - i + y - k)
                add(x - i + 1, x - i + 1 + n - y)
            elif i < (x + y) // 2:
                k = i + (y - x + 1) // 2
                add(1, k - i)
                add(i - x + 2, i - x + y - k)
                add(i - x + 1, i - x + 1 + n - y)
            else:
                add(1, n - i)

        return list(accumulate(diff))[1:]