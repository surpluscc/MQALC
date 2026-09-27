class Solution:
    def minimumLevel(self, root: Optional[TreeNode]) -> int:
        ans, s = -1, inf
        q = deque()
        q.append(root)
        floor = 1
        while q:
            size, tmp = len(q), 0
            for i in range(size):
                node = q.popleft()
                tmp += node.val
                if node.left:
                    q.append(node.left)
                if node.right:
                    q.append(node.right)
            if tmp < s:
                s = tmp
                ans = floor
            floor += 1
        return ans