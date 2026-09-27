class Solution:
    def simulationResult(self, windows: List[int], queries: List[int]) -> List[int]:
        n = len(windows)
        order = list()
        activated = set()
        for i in range(len(queries) - 1, -1, -1):
            window = queries[i]
            if window not in activated:
                activated.add(window)
                order.append(window)
        for i in range(n):
            window = windows[i]
            if window not in activated:
                order.append(window)
        return order
