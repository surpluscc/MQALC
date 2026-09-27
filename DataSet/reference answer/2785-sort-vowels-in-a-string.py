class Solution:
    def sortVowels(self, s: str) -> str:
        vowels = {'a', 'e', 'i', 'o', 'u', 'A', 'E', 'I', 'O', 'U'}
        cnt = [-1] * 58
        for ch in vowels:
            cnt[ord(ch) - ord('A')] = 0
        
        for ch in s:
            i = ord(ch) - ord('A')
            if cnt[i] != -1:
                cnt[i] += 1
        
        s_list = list(s)
        idx = 0
        for i in range(len(s_list)):
            ch = s_list[i]
            pos = ord(ch) - ord('A')
            if cnt[pos] != -1:
                while cnt[idx] <= 0:
                    idx += 1
                s_list[i] = chr(idx + ord('A'))
                cnt[idx] -= 1
        
        return ''.join(s_list)