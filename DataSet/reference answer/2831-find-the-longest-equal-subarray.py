class Solution:
    def longestEqualSubarray(self, nums: List[int], k: int) -> int:
        pos = defaultdict(list)
        for i, num in enumerate(nums):
            pos[num].append(i)

        ans = 0
        for vec in pos.values():
            j = 0
            for i in range(len(vec)):
                # 缩小窗口，直到不同元素数量小于等于 k 
                while vec[i] - vec[j] - (i - j) > k:
                    j += 1
                ans = max(ans, i - j + 1)

        return ans