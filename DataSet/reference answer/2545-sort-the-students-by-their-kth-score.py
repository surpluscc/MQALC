class Solution:
    def sortTheStudents(self, score: List[List[int]], k: int) -> List[List[int]]:
        # 也可以写成 score.sort(key=lambda row: -row[k])
        score.sort(key=lambda row: row[k], reverse=True)
        return score