class Solution:
    def minOperations(self, nums: List[int], x: int, y: int) -> int:
        left, right = 1, max(nums) // y + 1
        x -= y
        while left <= right:
            mid = (left + right) >> 1
            s = mid
            for v in nums:
                t = (v + y - 1) // y
                if mid >= t:
                    continue
                s -= (v - mid * y + x - 1) // x
                if s < 0:
                    break
            if s >= 0:
                right = mid - 1
            else:
                left = mid + 1
        return right + 1