class Solution:
    def sumRemoteness(self, grid: list[list[int]]) -> int:
        # Direction arrays for moving up, down, left, right
        self.dir = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        n = len(grid)

        # Calculate total sum of all non-blocked cells
        total_sum = sum(val for row in grid for val in row if val != -1)

        # Calculate remoteness for each non-blocked cell
        result = 0
        for row in range(n):
            for col in range(n):
                if grid[row][col] > 0:
                    # arr[0] = sum of reachable cells
                    # arr[1] = count of reachable cells
                    arr = [0, 0]
                    self._dfs(grid, row, col, arr)
                    result += (total_sum - arr[0]) * arr[1]

        return result

    # DFS to find sum and count of all cells reachable from (row, col)
    def _dfs(
        self, grid: list[list[int]], row: int, col: int, arr: list
    ) -> None:
        arr[0] += grid[row][col]  # Add current cell value to sum
        arr[1] += 1  # Increment reachable cells count
        grid[row][col] = -1  # Mark as visited

        # Explore all 4 directions
        for di, dj in self.dir:
            new_row, new_col = row + di, col + dj
            if self._is_valid(grid, new_row, new_col):
                self._dfs(grid, new_row, new_col, arr)

    # Checks if cell (row, col) is within grid bounds and not blocked/visited
    def _is_valid(self, grid: list[list[int]], row: int, col: int) -> bool:
        n = len(grid)
        return 0 <= row < n and 0 <= col < n and grid[row][col] > 0