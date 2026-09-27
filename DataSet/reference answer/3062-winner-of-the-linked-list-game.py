class Solution:
    def gameResult(self, head: Optional[ListNode]) -> str:
        even = head
        even_points = 0
        odd_points = 0

        # Traverse through the linked list assigning points
        while even is not None:
            odd = even.next
            if even.val > odd.val:
                even_points += 1
            else:
                odd_points += 1
            even = odd.next
            
        # Return the winning team
        if odd_points > even_points:
            return "Odd"
        elif odd_points < even_points:
            return "Even"
        else:
            return "Tie"