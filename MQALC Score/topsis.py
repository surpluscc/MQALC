import numpy as np
import pandas as pd

# ==========================================
# 1. 数据准备 (Data Preparation)
# ==========================================
models = ["Reference Answer", "Chatgpt-3.5-turbo", "Chatgpt-5.1-推理", "Chatgpt-5.1-不推理", "Deepseek-v3.2"]
indicators = ["执行时间", "峰值内存", "认知复杂度CoC", "可维护性MI"]

# 原始数据矩阵
raw_data = np.array([
    [0.019942, 0.9485, 5.52, 68.88],  # Reference Answer
    [0.034703, 0.9836, 5.58, 71.68],  # Chatgpt-3.5-turbo
    [0.028171, 1.0210, 7.32, 66.26],  # Chatgpt-5.1-推理
    [0.021771, 1.0244, 7.65, 69.48],  # Chatgpt-5.1-不推理
    [0.025434, 0.9005, 7.15, 64.06]   # Deepseek-v3.2
])

df_raw = pd.DataFrame(raw_data, index=models, columns=indicators)

# ==========================================
# 2. 极差标准化 (Min-Max Normalization) - 关键修正
# ==========================================
# 这一步将所有数据映射到 [0, 1] 区间
# 0 代表该列最差，1 代表该列最好
# 这样消除了“底数”影响，MI指标的权重会恢复正常

norm_data = raw_data.copy()

# A. 处理成本型指标 (越小越好): 执行时间(0), 内存(1), CoC(2)
# 公式: (Max - x) / (Max - Min)
for i in [0, 1, 2]:
    col_min = raw_data[:, i].min()
    col_max = raw_data[:, i].max()
    norm_data[:, i] = (col_max - raw_data[:, i]) / (col_max - col_min)

# B. 处理效益型指标 (越大越好): MI(3)
# 公式: (x - Min) / (Max - Min)
i = 3
col_min = raw_data[:, i].min()
col_max = raw_data[:, i].max()
norm_data[:, i] = (raw_data[:, i] - col_min) / (col_max - col_min)

df_norm = pd.DataFrame(norm_data, index=models, columns=indicators)

# ==========================================
# 3. 熵权法确定权重 (Entropy Weight Method)
# ==========================================
# 计算比重 P (因为已经是0-1归一化，且可能含0，需要平移处理避免log(0))
# 这里我们采用一种简单的平移方法：每个值 + 0.001 (微小量)
shifted_data = norm_data + 0.001 
P = shifted_data / shifted_data.sum(axis=0)

# 计算熵值 e
k = 1 / np.log(len(models))
e = -k * np.sum(P * np.log(P), axis=0)

# 计算差异系数 d
d = 1 - e

# 计算权重 w
weights = d / d.sum()

# 打印新权重
print("--- 修正后的权重分配 (基于Min-Max) ---")
for name, w in zip(indicators, weights):
    print(f"{name}: {w:.4f}")

# ==========================================
# 4. TOPSIS 计算 (Calculation)
# ==========================================
# 加权矩阵
Z = norm_data * weights

# 确定正负理想解 (因为已经Min-Max归一化，理想解就是加权后的最大值)
Z_plus = Z.max(axis=0)
Z_minus = Z.min(axis=0)

# 计算欧氏距离
D_plus = np.sqrt(np.sum((Z - Z_plus)**2, axis=1))
D_minus = np.sqrt(np.sum((Z - Z_minus)**2, axis=1))

# 计算综合得分 Score = D- / (D+ + D-)
scores = D_minus / (D_plus + D_minus)

# ==========================================
# 5. 结果输出
# ==========================================
df_result = pd.DataFrame({
    "模型": models,
    "TOPSIS得分": scores
})

# 按得分降序排列
df_result = df_result.sort_values(by="TOPSIS得分", ascending=False).reset_index(drop=True)
df_result.index = df_result.index + 1
df_result.index.name = "排名"

print("\n--- 最终评估结果 ---")
print(df_result)