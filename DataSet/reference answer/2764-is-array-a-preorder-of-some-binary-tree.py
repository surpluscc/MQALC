
class Solution:
    def isPreorder(self, nodes: List[List[int]]) -> bool:
        stack=[-1]
        for i,j in nodes:
            while stack and stack[-1]!=j:
                stack.pop()
            if not stack:
                return False
            stack.append(i)
        return True