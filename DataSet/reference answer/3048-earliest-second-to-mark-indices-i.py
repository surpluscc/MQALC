class Solution:
    def earliestSecondToMarkIndices(self, nums: List[int], changeIndices: List[int]) -> int:
        n, m = len(nums), len(changeIndices)
        if n > m:
            return -1

        def check(mx: int) -> bool:
            last_t = [-1] * n
            for t, idx in enumerate(changeIndices[:mx]):
                last_t[idx - 1] = t
            if -1 in last_t:  # 有课程没有考试时间
                return False

            cnt = 0
            for i, idx in enumerate(changeIndices[:mx]):
                idx -= 1
                if i == last_t[idx]:  # 考试
                    if nums[idx] > cnt:  # 没时间复习
                        return False
                    cnt -= nums[idx]  # 复习这门课程
                else:
                    cnt += 1  # 留着后面用
            return True

        left = n + sum(nums)
        ans = left + bisect_left(range(left, m + 1), True, key=check)
        return -1 if ans > m else ans