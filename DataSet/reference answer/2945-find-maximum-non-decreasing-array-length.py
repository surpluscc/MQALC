class Solution:
    def findMaximumLength(self, nums: List[int]) -> int:
        n = len(nums)
        s = list(accumulate(nums, initial=0))
        f = [0] * (n + 1)
        last = [0] * (n + 1)
        q = deque([0])
        for i in range(1, n + 1):
            # 1. 去掉队首无用数据（计算转移时，直接取队首）
            while len(q) > 1 and s[q[1]] + last[q[1]] <= s[i]:
                q.popleft()
            
            # 2. 计算转移
            f[i] = f[q[0]] + 1
            last[i] = s[i] - s[q[0]]
            
            # 3. 去掉队尾无用数据
            while q and s[q[-1]] + last[q[-1]] >= s[i] + last[i]:
                q.pop()
            q.append(i)
        return f[n]