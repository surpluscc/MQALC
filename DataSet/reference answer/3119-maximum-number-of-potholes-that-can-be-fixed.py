class Solution:
    def maxPotholes(self, road: str, budget: int) -> int:
        res = []#统计连续X的个数
        ans, tmp = 0, 0
        for c in road:
            if c == ".":
                if tmp:
                    res.append(tmp)
                tmp = 0
                continue
            else:
                tmp += 1
        if tmp:
            res.append(tmp)
        res.sort(reverse=True)#从大到小排序
        for i in res:
            if i + 1 <= budget:
                ans += i
                budget -= i + 1
            else:
                ans += budget - 1
                budget = 0
            if budget == 0:
                break
        return ans
