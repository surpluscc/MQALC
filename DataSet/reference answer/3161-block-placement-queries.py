from sortedcontainers import SortedList

class Solution:
    def getResults(self, queries: List[List[int]]) -> List[bool]:
        m = max(q[1] for q in queries) + 1
        t = [0] * (2 << m.bit_length())

        # 把 i 处的值改成 val
        def update(o: int, l: int, r: int, i: int, val: int) -> None:
            if l == r:
                t[o] = val
                return
            m = (l + r) // 2
            if i <= m:
                update(o * 2, l, m, i, val)
            else:
                update(o * 2 + 1, m + 1, r, i, val)
            t[o] = max(t[o * 2], t[o * 2 + 1])

        # 查询 [0,R] 中的最大值
        def query(o: int, l: int, r: int, R: int) -> int:
            if r <= R:
                return t[o]
            m = (l + r) // 2
            if R <= m:
                return query(o * 2, l, m, R)
            return max(t[o * 2], query(o * 2 + 1, m + 1, r, R))

        sl = SortedList([0, m])  # 哨兵
        ans = []
        for q in queries:
            x = q[1]
            i = sl.bisect_left(x)
            pre = sl[i - 1]  # x 左侧最近障碍物的位置
            if q[0] == 1:
                nxt = sl[i]  # x 右侧最近障碍物的位置
                sl.add(x)
                update(1, 0, m, x, x - pre)    # 更新 d[x] = x - pre
                update(1, 0, m, nxt, nxt - x)  # 更新 d[nxt] = nxt - x
            else:
                # 最大长度要么是 [0,pre] 中的最大 d，要么是 [pre,x] 这一段的长度
                max_gap = max(query(1, 0, m, pre), x - pre)
                ans.append(max_gap >= q[2])
        return ans