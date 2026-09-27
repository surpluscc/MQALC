
class Solution:
  def colorRed(self, size: int) -> List[List[int]]:
      n, res_l = 2 * size, []
      for i in range(size, 1, -4):
          res_l += [[i, j] for j in range(1, n, 2)]
          if i >= 3: res_l.append([i - 1, 2])
          i -= 2
          if i >= 2: res_l += [[i, j] for j in range(3, n - 4, 2)]
          if i >= 3: res_l.append([i - 1, 1])
          i -= 2
          n -= 8
      res_l.append([1, 1])
      return res_l