class Solution:
    def longestCommonPrefix(self, arr1: List[int], arr2: List[int]) -> int:
        st = set()
        for x in arr1:
            while x:
                st.add(x)
                x //= 10

        mx = 0
        for x in arr2:
            while x and x not in st:
                x //= 10
            mx = max(mx, x)
        return len(str(mx)) if mx else 0