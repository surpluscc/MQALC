class Solution:
    def findPattern(self, board: List[List[int]], pattern: List[str]) -> List[int]:
        pm, pn = len(pattern), len(pattern[0])
        m, n = len(board), len(board[0])
        for i in range(m - pm + 1):
            for j in range(n - pn + 1):
                d = defaultdict(int)
                s = set()
                check = True
                for a in range(pm):
                    for b in range(pn):
                        c = pattern[a][b]
                        if c.isdigit() and board[i + a][j + b] != int(c):
                            check = False
                        if c.isalpha():
                            if c in d:
                                if d[c] != board[i + a][j + b]:
                                    check = False
                            else:
                                if board[i + a][j + b] not in s:
                                    d[c] = board[i + a][j + b]
                                    s.add(board[i + a][j + b])
                                else:
                                    check = False
                if check:
                    return [i, j]
        return [-1, -1]
