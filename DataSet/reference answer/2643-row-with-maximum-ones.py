class Solution:
    def rowAndMaximumOnes(self, mat: List[List[int]]) -> List[int]:
        row_idx = max_sum = -1
        for i, row in enumerate(mat):
            s = sum(row)
            if s > max_sum:
                row_idx, max_sum = i, s
        return [row_idx, max_sum]