import json
import random
import time
import os
import re
from tqdm import tqdm
from openai import OpenAI

# ==========================================================
# 1. 配置区域
# ==========================================================
INPUT_FILE = "merged_for_agent_eval.json"   # 预处理好的数据文件
OUTPUT_FILE = "agent_ranking_results.json"  # 结果保存文件

# 初始化 OpenAI 客户端 (适配 API)
client = OpenAI(

    api_key="",  # ⚠️ 请在此处填入你的API Key
    base_url=""
)

# 模型配置
TARGET_MODEL = 'gpt-5.5'

# ==========================================================
# 2. 核心功能函数
# ==========================================================

def construct_prompt(problem_info, shuffled_candidates):
    """
    构建“零干扰”提示词：不告诉具体标准，让Agent暴露原始偏好
    """
    candidates_text = ""
    for alias, code in shuffled_candidates:
        # 简单截断防止超长 (一般LeetCode代码不会超，只是保险)
        safe_code = code[:10000] 
        candidates_text += f"[{alias}]\n```python\n{safe_code}\n```\n\n"

    # 最终极简版 Prompt
    prompt = f"""
You are a **Senior Code Evaluator**.
I have 5 Python solutions for the problem: "{problem_info['problem_slug']}".

**Task:**
Rank these solutions from BEST to WORST based on your expert judgment of **General Code Quality**.

**Note:**
- Evaluate purely based on **static analysis** of the code text.
- **Output strictly a JSON object** containing the ranking list.
- **NO explanation**, **NO scores**, **NO extra text**.

Here are the anonymous solutions (labeled A-E):
{candidates_text}

### REQUIRED OUTPUT FORMAT
{{
    "ranking": ["Solution_X", "Solution_Y", "Solution_Z", "Solution_W", "Solution_V"]
}}
"""
    return prompt

def get_model_response(prompt_content, model=TARGET_MODEL):
    """
    调用 API 获取结果
    """
    try:
        messages = [{"role": "user", "content": prompt_content}]
        
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=0, # 设为0以保证结果的可复现性和严谨性
        )
        # 提取文本内容
        return response.choices[0].message.content
        
    except Exception as e:
        print(f"\n❌ API 调用异常: {e}")
        return None

def parse_ranking(response_text):
    """
    解析返回的 JSON，提取 ranking 列表
    """
    if not response_text:
        return None
        
    # 1. 尝试直接解析 JSON
    try:
        data = json.loads(response_text)
        if "ranking" in data and isinstance(data["ranking"], list):
            return data["ranking"]
    except:
        pass

    # 2. 如果包含在 Markdown 代码块中，正则提取
    try:
        # 寻找 "ranking": ["...", "..."] 这样的结构
        match = re.search(r'"ranking"\s*:\s*(\[[^\]]+\])', response_text, re.DOTALL)
        if match:
            list_str = match.group(1)
            return json.loads(list_str)
    except:
        pass
    
    # 3. 最后的兜底：寻找 JSON 块
    try:
        match = re.search(r"```(?:json)?\s*(.*?)\s*```", response_text, re.DOTALL)
        if match:
            return json.loads(match.group(1)).get("ranking")
    except:
        pass

    return None

# ==========================================================
# 3. 主执行流程 (Pipeline)
# ==========================================================

def run_evaluation():
    # --- 1. 读取源数据 ---
    if not os.path.exists(INPUT_FILE):
        print(f"❌ 找不到输入文件 {INPUT_FILE}，请先运行预处理脚本。")
        return

    with open(INPUT_FILE, 'r', encoding='utf-8') as f:
        problems = json.load(f)

    # --- 2. 断点续传检查 ---
    results = []
    processed_ids = set()
    
    if os.path.exists(OUTPUT_FILE):
        with open(OUTPUT_FILE, 'r', encoding='utf-8') as f:
            try:
                results = json.load(f)
                processed_ids = {item['problem_id'] for item in results}
                print(f"🔄 检测到 {len(processed_ids)} 条已完成记录，将自动跳过。")
            except:
                print("⚠️ 结果文件格式错误，重新开始。")

    # 筛选出未处理的任务
    tasks = [pid for pid in problems if pid not in processed_ids]
    
    if not tasks:
        print("✅ 所有题目已评估完毕！")
        return

    print(f"🚀 开始评估剩余 {len(tasks)} 条数据 (Model: {TARGET_MODEL})...")

    # --- 3. 循环处理 ---
    for pid in tqdm(tasks, desc="Evaluating"):
        data = problems[pid]
        
        # === A. 混淆 (Shuffle) & 匿名化 ===
        original_codes = data['codes'] # {"Deepseek": "code...", "GPT": "code..."}
        
        # 生成匿名代号
        aliases = ["Solution_A", "Solution_B", "Solution_C", "Solution_D", "Solution_E"]
        
        # 转为列表并随机打乱
        items = list(original_codes.items())
        random.shuffle(items) # <--- 关键：去除位置偏见
        
        current_mapping = {}      # 映射表: Alias -> Real Name
        shuffled_input = []       # 发给Agent的: (Alias, Code)
        
        for idx, (real_name, code) in enumerate(items):
            alias = aliases[idx]
            current_mapping[alias] = real_name
            shuffled_input.append((alias, code))
            
        # === B. 构建 Prompt 并调用 API ===
        prompt = construct_prompt(data['info'], shuffled_input)
        
        # 简单的重试机制
        ranking_result = None
        for attempt in range(3):
            response_text = get_model_response(prompt)
            ranking_result = parse_ranking(response_text)
            
            if ranking_result and len(ranking_result) == 5:
                break # 成功拿到结果
            else:
                # print(f"⚠️ 解析失败或格式错误 (Attempt {attempt+1}), 重试...")
                time.sleep(1)
        
        if not ranking_result:
            print(f"❌ 题目 {pid} 3次重试失败，跳过。")
            continue

        # === C. 还原 (De-anonymize) 并保存 ===
        try:
            # 将 [Solution_B, Solution_A...] 还原为 [Deepseek, ChatGPT...]
            real_ranking = [current_mapping[alias] for alias in ranking_result]
            
            result_entry = {
                "problem_id": pid,
                "problem_slug": data['info']['problem_slug'],
                "winner": real_ranking[0], # 第一名
                "ranking": real_ranking    # 完整排名
            }
            results.append(result_entry)
            
            # 实时写盘，防止数据丢失
            with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
                json.dump(results, f, ensure_ascii=False, indent=2)
                
        except Exception as e:
            print(f"❌ 数据还原错误 {pid}: {e}")

        # 稍微延时，避免触发 API 速率限制 (根据你的API限制调整)
        time.sleep(0.5)

    print(f"\n🎉 评估全部完成！结果已保存在 {OUTPUT_FILE}")

if __name__ == "__main__":
    run_evaluation()