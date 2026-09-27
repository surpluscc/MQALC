import numpy as np
import pandas as pd

# ==========================================
# 1. 基础数据录入
# ==========================================

models = [
    "GPT-5.1-Reasoning",
    "GPT-5.1-NoReasoning",
    "GPT-3.5-Turbo",
    "DeepSeek-V3.2",
    "DeepSeek-V4",
    "Gemini-3.5-Flash",
    "GLM-5.2",
    "Grok-4.3",
    "Qwen3.7-Plus"
]

# 优化前数据
# 每列依次为：
# [执行时间 ET(ms), 峰值内存 MU(KB), 认知复杂度 CoC, 可维护性 MI]
data_before = np.array([
    [0.2940, 8.2540, 10.780, 65.190],  # GPT-5.1-Reasoning
    [0.1840, 3.8830,  9.920, 69.870],  # GPT-5.1-NoReasoning
    [0.0720, 1.0050,  5.890, 70.740],  # GPT-3.5-Turbo
    [0.2880, 3.4020,  8.770, 61.230],  # DeepSeek-V3.2
    [0.2828, 3.7335,  9.220, 79.860],  # DeepSeek-V4
    [0.1303, 1.5631,  8.960, 80.740],  # Gemini-3.5-Flash
    [0.2757, 7.2484,  9.820, 75.770],  # GLM-5.2
    [0.2941, 8.1072, 11.140, 60.000],  # Grok-4.3
    [0.1024, 4.9448,  9.930, 75.070]   # Qwen3.7-Plus
], dtype=float)

# 优化后数据
# 每列依次为：
# [执行时间 ET(ms), 峰值内存 MU(KB), 认知复杂度 CoC, 可维护性 MI]
data_after = np.array([
    [0.2140, 5.3200,  9.840, 62.650],  # GPT-5.1-Reasoning
    [0.1500, 3.2590, 10.140, 62.410],  # GPT-5.1-NoReasoning
    [0.0360, 0.9000,  5.600, 70.780],  # GPT-3.5-Turbo
    [0.2400, 2.8030,  8.060, 63.810],  # DeepSeek-V3.2
    [0.2793, 3.2644,  8.020, 67.760],  # DeepSeek-V4
    [0.0985, 1.4544,  8.000, 72.010],  # Gemini-3.5-Flash
    [0.2721, 6.9477,  7.630, 63.970],  # GLM-5.2
    [0.2105, 7.9168,  8.160, 61.800],  # Grok-4.3
    [0.0437, 4.8892,  8.700, 62.880]   # Qwen3.7-Plus
], dtype=float)



# ⚠️ 注意：这里必须填入您在 RQ1/RQ2 阶段计算出的【最终定稿权重】！
# 这里暂用我之前根据您的文本提取的修正后权重作为示例：
weights = np.array([0.1688, 0.3424, 0.2978, 0.1910])

# ==========================================
# 2. 绝对锚点构建 (Absolute Bounds)
# ==========================================
# 格式: 字典 key -> (Ideal_best 理想最优解, Boundary_worst 理论最差解)
# 这里的设定必须与您画雷达图时使用的边界保持严格一致！
bounds = {
    0: (0.0, 0.35),   # Time (越小越好：0.0是完美，0.35是极差底线)
    1: (0.0, 9.0),    # Mem (越小越好：0.0是完美，9.0是极差底线)
    2: (4.0, 12.0),   # CoC (越小越好：4.0是完美，12.0是极差底线)
    3: (100.0, 50.0)  # MI  (越大越好：100是完美，50是极差底线)
}

def apply_absolute_norm(data_matrix):
    """
    基于绝对物理标尺将数据投影到 [0, 1] 空间
    """
    norm_matrix = np.zeros_like(data_matrix)
    for i in range(4):
        ideal, boundary = bounds[i]
        
        # 统一映射公式: (最差边界值 - 当前实际值) / (最差边界值 - 理想最优值)
        # 这样无论成本型还是效益型指标，算出来都是越大越好（靠近1代表靠近Ideal）
        score = (boundary - data_matrix[:, i]) / (boundary - ideal)
        
        # 截断处理 (Clipping)，防止极个别超常数据导致越界
        norm_matrix[:, i] = np.clip(score, 0.0, 1.0)
        
    return norm_matrix

# 对前后数据分别进行绝对归一化
norm_before = apply_absolute_norm(data_before)
norm_after = apply_absolute_norm(data_after)

# ==========================================
# 3. 静态 TOPSIS 得分计算
# ==========================================
# 在绝对归一化体系下，坐标系已被固定：
# 正理想解(最强王者) 永远是各维度都拿满分(1.0)，加权后即为 weights 本身
# 负理想解(最强青铜) 永远是各维度都拿0分(0.0)，加权后即为 0向量
Z_plus = weights
Z_minus = np.zeros_like(weights)

def calculate_topsis_score(norm_matrix):
    # 步骤1：数据矩阵加权
    Z = norm_matrix * weights
    
    # 步骤2：计算到正、负理想解的欧氏距离
    D_plus = np.sqrt(np.sum((Z - Z_plus)**2, axis=1))
    D_minus = np.sqrt(np.sum((Z - Z_minus)**2, axis=1))
    
    # 步骤3：计算贴近度 (得分)
    return D_minus / (D_plus + D_minus)

scores_before = calculate_topsis_score(norm_before)
scores_after = calculate_topsis_score(norm_after)

# ==========================================
# 4. 结果整理与输出
# ==========================================
df_result = pd.DataFrame({
    "模型 (Model)": models,
    "优化前 TOPSIS": scores_before,
    "优化后 TOPSIS": scores_after
})

# 计算净增益与提升率
df_result["净增益 (Delta)"] = df_result["优化后 TOPSIS"] - df_result["优化前 TOPSIS"]
df_result["提升率 (%)"] = (df_result["净增益 (Delta)"] / df_result["优化前 TOPSIS"] * 100)

# 为了在控制台输出美观，进行格式化
df_result_formatted = df_result.copy()
df_result_formatted["优化前 TOPSIS"] = df_result["优化前 TOPSIS"].map("{:.4f}".format)
df_result_formatted["优化后 TOPSIS"] = df_result["优化后 TOPSIS"].map("{:.4f}".format)
df_result_formatted["净增益 (Delta)"] = df_result["净增益 (Delta)"].map("{:+.4f}".format)
df_result_formatted["提升率 (%)"] = df_result["提升率 (%)"].map("{:+.2f}%".format)

print("\n" + "="*60)
print(" 🚀 基于绝对物理标尺的 TOPSIS 纵向优化评估结果 🚀")
print("="*60)
print(df_result_formatted.to_string(index=False))
print("="*60)
print("\n[注] 本计算严格冻结了评价权重与极值边界，排除了数据集异质性干扰，增益具备绝对数学意义。")