class Solution:
    def isItPossible(self, word1: str, word2: str) -> bool:
        c1 = Counter(word1)
        c2 = Counter(word2)
        for x, c in c1.items():
            for y, d in c2.items():
                if y == x:  # 无变化
                    if len(c1) == len(c2):
                        return True
                elif len(c1) - (c == 1) + (y not in c1) == \
                     len(c2) - (d == 1) + (x not in c2):  # 基于长度计算变化量
                    return True
        return False