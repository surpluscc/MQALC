class Solution:
    def minimumDistance(
        self, n: int, edges: list[list[int]], s: int, marked: list[int]
    ) -> int:
        # Convert marked array to set for O(1) lookups
        mark_set = set(marked)

        # Build adjacency list representation of the graph
        adj = defaultdict(list)
        for u, v, w in edges:
            adj[u].append((v, w))

        # Distance dictionary initialized only for `s`
        dist = {s: 0}

        # Min heap prioritized by distance
        min_heap = [(0, s)]

        # Dijkstra's algorithm
        while min_heap:
            distance, node = heapq.heappop(min_heap)

            # Found a marked node, return its distance
            if node in mark_set:
                return dist[node]

            # Explore neighbors
            for next_node, weight in adj[node]:
                new_dist = distance + weight

                # If we found a shorter path, update and add to the priority queue
                if new_dist < dist.get(next_node, float("inf")):
                    dist[next_node] = new_dist
                    heapq.heappush(min_heap, (new_dist, next_node))

        # No path found to any marked node
        return -1