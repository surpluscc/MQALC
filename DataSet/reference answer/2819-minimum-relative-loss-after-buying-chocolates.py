class Solution:
    def minimumRelativeLosses(self, prices: List[int], queries: List[List[int]]) -> List[int]:
        n = len(prices)
        prices.sort()
        psum = [0] * (n + 1)
        for i, x in enumerate(prices):
            psum[i + 1] = psum[i] + x
        
        res = []
        for i, (k, m) in enumerate(queries):
            if m == n:
                x = bisect_right(prices, k)
                res.append(psum[x] + 2 * k * (n - x) - (psum[n] - psum[x]))
                continue
                
            need, idx = n - m, m
            lo, hi = 0, m - 1
            while lo <= hi:
                mid = (lo + hi) >> 1
                if k - prices[mid] > prices[mid + need] - k:
                    lo = mid + 1
                else:
                    hi, idx = mid - 1, mid
            left = psum[idx]
            right = 2 * k * (n - idx - need) - (psum[n] - psum[idx + need])
            res.append(left + right)
        return res