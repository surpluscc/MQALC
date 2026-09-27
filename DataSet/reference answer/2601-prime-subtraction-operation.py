MX = 1000
P = [0]  # 哨兵，避免二分越界
is_prime = [True] * MX
for i in range(2, MX):
    if is_prime[i]:
        P.append(i)  # 预处理质数列表
        for j in range(i * i, MX, i):
            is_prime[j] = False

class Solution:
    def primeSubOperation(self, nums: List[int]) -> bool:
        pre = 0
        for x in nums:
            if x <= pre: return False
            pre = x - P[bisect_left(P, x - pre) - 1]  # 减去 < x-pre 的最大质数
        return True