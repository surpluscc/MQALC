class Solution:
    def minimumCost(self, start: List[int], target: List[int], specialRoads: List[List[int]]) -> int:
        t = tuple(target)
        dis = defaultdict(lambda: inf)
        dis[tuple(start)] = 0
        vis = set()
        while True:
            v, dv = None, -1
            for p, d in dis.items():
                if p not in vis and (dv < 0 or d < dv):
                    v, dv = p, d
            if v == t: return dv  # 到终点的最短路已确定
            vis.add(v)
            vx, vy = v
            dis[t] = min(dis[t], dv + t[0] - vx + t[1] - vy)  # 更新到终点的最短路
            for x1, y1, x2, y2, cost in specialRoads:
                w = (x2, y2)
                dis[w] = min(dis[w], dv + abs(x1 - vx) + abs(y1 - vy) + cost)