class Solution:
    def minimumOperations(self, nums: List[int], target: List[int]) -> int:
        pos_sum = neg_sum = 0
        d = target[0] - nums[0]
        if d > 0:
            pos_sum = d
        else:
            neg_sum = -d
        for (n1, t1), (n2, t2) in pairwise(zip(nums, target)):
            d = (t2 - n2) - (t1 - n1)
            if d > 0:
                pos_sum += d
            else:
                neg_sum -= d
        return max(pos_sum, neg_sum)