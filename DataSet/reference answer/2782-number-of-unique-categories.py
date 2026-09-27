class Solution:
    def numberOfCategories(self, n: int, categoryHandler: Optional['CategoryHandler']) -> int:
        dc = set()
        for i in range(n):
            for j in dc:
                if categoryHandler.haveSameCategory(i,j): break
            else: dc.add(i)
        return len(dc)