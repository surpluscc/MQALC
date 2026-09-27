class Solution:
    def mostFrequentPrime(self, mat: List[List[int]]) -> int:
        m, n = len(mat), len(mat[0])
        cnt = Counter()
        for i, row in enumerate(mat):
            for j, v in enumerate(row):
                for dx, dy in (1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1), (1, -1):
                    x, y, val = i + dx, j + dy, v
                    while 0 <= x < m and 0 <= y < n:
                        val = val * 10 + mat[x][y]
                        # 如果 val 在 cnt 中，那么 val 一定是质数
                        if val in cnt or self.is_prime(val):
                            cnt[val] += 1
                        x += dx
                        y += dy

        ans, max_cnt = -1, 0
        for v, c in cnt.items():
            if c > max_cnt:
                ans, max_cnt = v, c
            elif c == max_cnt:
                ans = max(ans, v)
        return ans

    def is_prime(self, n: int) -> bool:
        return all(n % i for i in range(2, isqrt(n) + 1))