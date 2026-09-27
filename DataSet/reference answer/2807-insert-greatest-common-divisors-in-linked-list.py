class Solution:
    def insertGreatestCommonDivisors(self, head: Optional[ListNode]) -> Optional[ListNode]:
        node = head
        while node.next is not None:
            node.next = ListNode(math.gcd(node.val, node.next.val), node.next)
            node = node.next.next
        return head