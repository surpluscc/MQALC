class Solution:
    def numberOfSpecialSubstrings(self, s: str) -> int:
        substring_count = 0

        start = 0
        freq = [0] * 26
        for end in range(len(s)):
            freq[ord(s[end]) - ord("a")] += 1

            while freq[ord(s[end]) - ord("a")] > 1:
                freq[ord(s[start]) - ord("a")] -= 1
                start += 1

            substring_count += end - start + 1

        return substring_count