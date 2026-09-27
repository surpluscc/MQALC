class Solution:
    def survivedRobotsHealths(self, positions: List[int], healths: List[int], directions: str) -> List[int]:
        n = len(positions)
        a = sorted(zip(range(n), positions, healths, directions), key=lambda p: p[1])
        to_left = []
        st = []
        for i, _, h, d in a:
            if d == 'R':  # 向右，存入栈中
                st.append([i, h])
                continue
            # 当前机器人向左，与栈中向右的机器人碰撞
            while st:
                top = st[-1]
                if top[1] > h:  # 栈顶的健康度大
                    top[1] -= 1
                    break
                if top[1] == h:  # 健康度一样大
                    st.pop()
                    break
                h -= 1  # 当前机器人的健康度大
                st.pop()  # 移除栈顶
            else:  # while 循环没有 break，说明当前机器人把栈中的全部撞掉
                to_left.append([i, h])
        to_left += st  # 合并剩余的机器人
        to_left.sort(key=lambda p: p[0])  # 按编号排序
        return [h for _, h in to_left]