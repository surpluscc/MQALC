class Solution:
    def findWordsContaining(self, words: List[str], x: str) -> List[int]:
        return [i for i, s in enumerate(words) if x in s]