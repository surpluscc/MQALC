class Solution:
    def countGreatEnoughNodes(self, root: TreeNode, k: int) -> int:

        def dfs(node):
            if not node: return []

            arr = sorted(dfs(node.left ) +
                         dfs(node.right))[:k]

            if len(arr) >= k and arr[-1] < node.val:
                self.ans+= 1
            else:
                arr.append(node.val)

            return arr


        self.ans = 0
        dfs(root)
        return self.ans