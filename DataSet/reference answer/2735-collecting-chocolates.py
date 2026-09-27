class Solution:
    def minCost(self, nums: List[int], x: int) -> int:
        n = len(nums)
        # 找出 nums 中最小的元素，并用其为首元素构造一个新的数组
        min_idx = nums.index(min(nums))
        nums = nums[min_idx:] + nums[:min_idx]

        L = [n - 1] + [0] * (n - 1)
        # 循环来看，右侧 nums[0] 是更小的元素，但不一定是第一个更小的元素，需要用单调栈计算得到
        R = [n - i - 1 for i in range(n)]

        s = [0]
        for i in range(1, n):
            while s and nums[i] < nums[s[-1]]:
                R[s[-1]] = i - s[-1] - 1
                s.pop()
            L[i] = i - s[-1] - 1
            s.append(i)
        
        F = [0] * n
        # 辅助函数，一次差分，将 F[l..r] 都增加 d
        def diff_once(l: int, r: int, d: int) -> None:
            if l > r:
                return
            if l < n:
                F[l] += d
            if r + 1 < n:
                F[r + 1] -= d
        
        # 辅助函数，二次差分，将 F[l..r] 增加 ki + b，i 是下标
        def diff_twice(l: int, r: int, k: int, b: int) -> None:
            if l > r:
                return
            diff_once(l, l, k * l + b)
            diff_once(l + 1, r, k)
            diff_once(r + 1, r + 1, -(k * r + b))

        # 进行操作需要的成本
        diff_twice(0, n - 1, x, 0)

        for i in range(n):
            minv, maxv = min(L[i], R[i]), max(L[i], R[i])
            # 第一种情况，窗口数量 k+1，总和 nums[i] * k + nums[i]
            diff_twice(0, minv, nums[i], nums[i])
            # 第二种情况，窗口数量 minv+1，总和 0 * k + nums[i] * (minv + 1)
            diff_twice(minv + 1, maxv, 0, nums[i] * (minv + 1))
            # 第三种情况，窗口数量 L[i]+R[i]-k+1，总和 -nums[i] * k + nums[i] * (L[i] + R[i] + 1)
            diff_twice(maxv + 1, L[i] + R[i], -nums[i], nums[i] * (L[i] + R[i] + 1))

        # 计算两次前缀和
        return min(accumulate(accumulate(F)))