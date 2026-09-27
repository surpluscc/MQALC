class Solution:
    def frequenciesOfElements(self, head: Optional[ListNode]) -> Optional[ListNode]:
        frequencies = {}
        current = head
        freq_head = None

        # Process the linked list, storing
        # frequency ListNodes in the hashtable 
        while current is not None:
            # Existing element, increment frequency 
            if current.val in frequencies:
                frequency_node = frequencies[current.val]
                frequency_node.val += 1

            # New element, create hashtable entry with frequency node
            else:
                new_frequency_node = ListNode(1, freq_head)
                frequencies[current.val] = new_frequency_node
                freq_head = new_frequency_node
            current = current.next

        return freq_head