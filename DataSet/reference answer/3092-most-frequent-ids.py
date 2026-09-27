class Solution:
    def mostFrequentIDs(self, nums: List[int], freq: List[int]) -> List[int]:
        ans = []
        cnt = Counter()
        h = []
        for x, f in zip(nums, freq):
            cnt[x] += f
            heappush(h, (-cnt[x], x))  # 取负号变成最大堆
            while -h[0][0] != cnt[h[0][1]]:  # 堆顶保存的数据已经发生变化
                heappop(h)  # 删除
            ans.append(-h[0][0])
        return ans