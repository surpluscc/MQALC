from openai import OpenAI
import os
import re
import json
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading

# ==========================================================
# 初始化 OpenAI 客户端
# ==========================================================
client = OpenAI(
    api_key="",  # 填入你的 API Key
    base_url=""
)


# ==========================================================
# 调用模型
# ==========================================================
def get_chatgpt_response(prompt, model='', temperature=0):
    response = client.chat.completions.create(
        model=model,
        messages=prompt,
        temperature=temperature,
    )
    return response


# ==========================================================
# 从模型输出中抽取代码
# ==========================================================
def get_code_from_response(text, language):
    if "```" not in text:
        return text.strip()

    if f"```{language}" in text:
        pattern = rf'```{language}(.*?)```'
    else:
        pattern = r'```(.*?)```'

    code_blocks = re.findall(pattern, text, re.DOTALL)
    return ''.join(code_blocks).strip()


# ==========================================================
# 处理单条任务：优化 passed.json 中的代码
# ==========================================================
def process_single_task(task_meta, output_dir, lang="python", max_retries=3):
    problem_id = task_meta["problem_id"]
    problem_slug = task_meta["problem_slug"]
    difficulty = task_meta.get("difficulty", "Unknown")
    estimated_date = task_meta.get("estimated_date", "")
    original_code = task_meta["generated_code"]
    language = task_meta["language"]

    # --------------------- 生成优化提示词（核心） ---------------------
    user_prompt = f"""
You will rewrite the following code into a strictly superior version while preserving 100% identical functionality, outputs, semantics, and edge-case behavior.

Before generating the final code, you must internally (silently) perform a structured chain-of-thought reasoning process with the following required sequence:

Identify all structural inefficiencies: unnecessary branches, deep nesting, redundant states, repeated expressions, temporary objects, and readability blockers.

Evaluate the impact of each inefficiency on:

Peak memory usage

Cognitive complexity (CoC)

Maintainability Index (MI)

Execution time

Plan a rewrite strategy that simultaneously improves all four metrics, without shifting tradeoffs (e.g., improving MI cannot worsen memory).

Rewrite the code following that plan, outputting only the final improved version.

Your reasoning must not appear in the output.

======================================================
MANDATORY IMPROVEMENTS (ALL FOUR METRICS)

Your rewritten version MUST demonstrate significant improvements in all of the following:

Peak memory usage — reduce allocations, shrink lifetimes, reduce intermediate objects

Cognitive complexity (CoC) — reduce nesting, reduce decision points, simplify logic

Maintainability Index (MI) — substantially increase

Execution time — optimize without violating (1)-(3)

All four metrics must improve. No metric may stay the same or degrade.

======================================================
EXTRA REQUIREMENTS TO STRENGTHEN MI IMPROVEMENT

To ensure that MI improves more strongly than with the previous prompt, the optimized code MUST:

reduce structural noise (e.g., redundant conditions, duplicated branches, unnecessary variables)

increase linear flow and flatten control structures

eliminate confusing or indirect logic

simplify expressions for better readability

reduce line count where possible without harming clarity

remove all hidden complexity drivers (implicit states, multi-step conditions, etc.)

ensure that each block of logic has a single clear purpose

These MI improvements must occur in addition to the reductions in memory usage, CoC, and execution time.

======================================================
ALLOWED TRANSFORMATIONS

You may perform any transformation that preserves exact behavior, including:

reorganizing control flow

merging or simplifying related conditions

removing intermediate variables

eliminating redundant computations

rewriting expressions to clearer, more maintainable forms

flattening nested logic into linear steps

combining multi-step operations into a single equivalent operation

reducing or eliminating temporary allocations

======================================================
STRICT DO-NOT-BREAK RULES

No algorithmic changes

No change in I/O, return types, exceptions, or edge-case behavior

No new branches or added nesting

No caching, memoization, or speculative precomputation

No clever tricks that reduce readability

No tradeoffs where improving one metric worsens another

======================================================
FINAL OUTPUT REQUIREMENTS

Output only the final optimized code

The optimized code must be executable and standalone

Every metric (memory, CoC, MI, execution time) must be strictly better

MI must improve more noticeably than with the original prompt

======================================================

Here is the code to optimize:


{original_code}
"""

    messages = [
        {"role": "system", "content": f"Your task is to optimize {lang} code."},
        {"role": "user", "content": user_prompt}
    ]

    # --------------------- 重试机制 ---------------------
    last_error = None
    for attempt in range(max_retries):
        try:
            response = get_chatgpt_response(messages)
            optimized_code = get_code_from_response(
                response.choices[0].message.content,
                lang
            )

            # 保存单个代码文件（可选）
            output_file = os.path.join(output_dir, f"{problem_id}-{problem_slug}.py")
            with open(output_file, "w", encoding="utf-8") as f:
                f.write(optimized_code)

            # 结构保持一致，只替换 generated_code
            new_item = {
                "problem_id": problem_id,
                "problem_slug": problem_slug,
                "difficulty": difficulty,
                "language": language,
                "generated_code": optimized_code,
                "estimated_date": estimated_date
            }

            return {
                "success": True,
                "data": new_item,
                "index": task_meta.get("_index", 0)
            }

        except Exception as e:
            last_error = str(e)
            time.sleep(1 * (attempt + 1))  # 递增等待

    return {
        "success": False,
        "error": last_error,
        "index": task_meta.get("_index", 0),
        "task_meta": task_meta # 返回原始meta以便记录失败信息
    }


# ==========================================================
# 主函数：并发优化 passed.json (支持断点续传)
# ==========================================================
def generate_code(output_dir, lang="python", max_workers=5, max_retries=3):
    tasks_meta_path = r"passed.json"  # 你的 passed.json 路径

    if not os.path.exists(tasks_meta_path):
        print(f"错误：找不到输入文件 {tasks_meta_path}")
        return

    with open(tasks_meta_path, "r", encoding="utf-8") as f:
        tasks_meta_lists = json.load(f)

    # 添加索引，保证输出顺序一致
    for idx, task_meta in enumerate(tasks_meta_lists):
        task_meta["_index"] = idx

    os.makedirs(output_dir, exist_ok=True)
    
    # =======================================================
    # 新增逻辑：断点续传设置
    # =======================================================
    # 定义进度文件：每次成功生成一条，就追加写入该文件
    progress_file = os.path.join(output_dir, "improved_passed_progress.jsonl")
    completed_ids = set()
    
    # 1. 检查已完成的任务
    if os.path.exists(progress_file):
        print(f"检测到进度文件 {progress_file}，正在读取历史进度...")
        with open(progress_file, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line:
                    try:
                        data = json.loads(line)
                        # 使用 problem_id 作为唯一标识
                        completed_ids.add(str(data['problem_id']))
                    except:
                        pass
        print(f"已跳过 {len(completed_ids)} 个已完成的任务。")

    # 2. 筛选出还需要做的任务
    tasks_to_do = [
        t for t in tasks_meta_lists 
        if str(t['problem_id']) not in completed_ids
    ]
    
    total_tasks = len(tasks_meta_lists)
    remaining_tasks = len(tasks_to_do)
    
    print(f"总任务数: {total_tasks}")
    print(f"剩余任务: {remaining_tasks}")
    
    # 如果已经全部完成，直接进入整合阶段
    if remaining_tasks == 0:
        print("所有任务已完成，准备整合结果...")
    else:
        print(f"开始并发处理... (Threads: {max_workers})")

    # --------------------- 多线程并发 ---------------------
    lock = threading.Lock() # 用于文件写入的锁
    
    if remaining_tasks > 0:
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_to_task = {
                executor.submit(
                    process_single_task, meta, output_dir, lang, max_retries
                ): meta
                for meta in tasks_to_do
            }

            count = 0
            for future in as_completed(future_to_task):
                result = future.result()
                
                if result["success"]:
                    count += 1
                    # 实时写入进度文件 (JSONL格式)
                    with lock:
                        with open(progress_file, 'a', encoding='utf-8') as f:
                            f.write(json.dumps(result["data"], ensure_ascii=False) + "\n")
                            f.flush() # 确保立即写入磁盘
                            
                    print(f"\r进度: {count}/{remaining_tasks} 已保存 - {result['data']['problem_slug'][:20]}", end="")
                else:
                    task_info = result.get('task_meta', {})
                    print(f"\n[失败] ID={task_info.get('problem_id')} Error={result['error']}")

    print("\n\n所有任务执行完毕，正在整合最终文件...")

    # =======================================================
    # 整合逻辑：读取完整进度文件并按原始顺序排序
    # =======================================================
    # 1. 读取所有已完成的数据（包括之前的和刚刚跑完的）
    final_data_map = {}
    if os.path.exists(progress_file):
        with open(progress_file, 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip():
                    try:
                        data = json.loads(line)
                        final_data_map[str(data['problem_id'])] = data
                    except:
                        pass
    
    # 2. 按照原始列表的顺序重建结果列表
    final_list = []
    missing_count = 0
    
    for task_meta in tasks_meta_lists:
        pid = str(task_meta['problem_id'])
        if pid in final_data_map:
            final_list.append(final_data_map[pid])
        else:
            # 如果某个任务最终还是失败了，这里可以选择跳过，或者填入原数据
            missing_count += 1
            pass

    # 3. 保存最终的 JSON 文件
    output_json = os.path.join(output_dir, "improved_passed.json")
    with open(output_json, "w", encoding="utf-8") as f:
        json.dump(final_list, f, ensure_ascii=False, indent=2)

    print(f"优化完成！")
    print(f"总计: {total_tasks}, 成功: {len(final_list)}, 缺失/失败: {missing_count}")
    print(f"最终结果已保存至: {output_json}")
    print(f"过程备份文件: {progress_file}")


# ==========================================================
# 主入口
# ==========================================================
if __name__ == "__main__":
    generate_code(
        output_dir="",
        lang="python",
        max_workers=5,
        max_retries=3
    )