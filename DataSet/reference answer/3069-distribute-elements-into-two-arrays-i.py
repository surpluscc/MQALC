class Solution:
    def resultArray(self, nums: List[int]) -> List[int]:
        a = nums[:1]
        b = nums[1:2]
        for x in nums[2:]:
            if a[-1] > b[-1]:
                a.append(x)
            else:
                b.append(x)
        return a + b