from openai import OpenAI
import os
import re
import json
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading

# ============================================================
# 1. API 配置 (保持原样)
# ============================================================
client = OpenAI(
    api_key="",  # 填入你的API Key
    base_url=""
)

def get_chatgpt_response(prompt, model='glm-5.2', temperature=0):
    """
    Returns the response from ChatGPT for a given prompt
    """
    response = client.chat.completions.create(
        model=model,
        messages=prompt,
        temperature=temperature,
    )
    return response

def get_code_from_response(text, language):
    if "```" not in text:
        return text.strip()

    if f"```{language}" in text:
        pattern = rf'```{language}(.*?)```'
    else:
        pattern = r'```(.*?)```'

    code_blocks = re.findall(pattern, text, re.DOTALL)
    return ''.join(code_blocks).strip()

def format_time(seconds):
    """格式化时间显示"""
    if seconds < 60:
        return f"{seconds:.1f}秒"
    elif seconds < 3600:
        return f"{seconds/60:.1f}分钟"
    else:
        return f"{seconds/3600:.1f}小时"

def process_single_task(task_meta, output_dir, lang="python", max_retries=3):
    """
    处理单个任务的代码生成，支持自动重试
    (逻辑保持不变)
    """
    task_id = task_meta['id']
    task_name = task_meta['name']
    task_description = task_meta['task_description']
    difficulty = task_meta.get('difficulty', 'Unknown')
    estimated_date = task_meta.get('estimated_date', '') 

    messages_prompt = f"Please provide a code implementation of the following description:\n{task_description}"
    template_key = f"{lang}_template"
    if template_key in task_meta:
        messages_prompt += f"\nProvide a valid {lang} code with this template:\n{task_meta[template_key]}"

    messages = [{"role": "system", "content": f"Your task is to write a {lang} program"}]
    messages.append({"role": "user", "content": messages_prompt})
    
    # 重试机制
    last_error = None
    for attempt in range(max_retries):
        try:
            response = get_chatgpt_response(messages)
            code = get_code_from_response(response.choices[0].message.content, lang)
            
            # 保存为单独的代码文件
            if lang == "python":
                output_file = os.path.join(output_dir, f"{task_id}-{task_name}.py")
            else:
                output_file = os.path.join(output_dir, f"{task_id}-{task_name}.java")

            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(code)

            # 构建 JSON 格式的结果
            language = "python3" if lang == "python" else "java"
            
            json_item = {
                "problem_id": task_id,
                "problem_slug": task_name,
                "difficulty": difficulty.capitalize(),
                "language": language,
                "generated_code": code,
                "estimated_date": estimated_date
            }
            
            # 注意：这里返回 data 用于写入 JSONL，同时返回 index 用于最后排序
            return {"success": True, "data": json_item, "task_name": task_name, "index": task_meta.get('_index', 0)}
        except Exception as e:
            last_error = str(e)
            if attempt < max_retries - 1:
                time.sleep(1 * (attempt + 1)) 
                continue
            else:
                return {"success": False, "error": last_error, "task_name": task_name, "task_id": task_id, "index": task_meta.get('_index', 0)}
    
    return {"success": False, "error": last_error, "task_name": task_name, "task_id": task_id, "index": task_meta.get('_index', 0)}


def generate_code(output_dir, lang="python", max_workers=5, max_retries=3):
    """
    Generates code from ChatGPT for a given code task
    修改为：支持断点续传和实时写入
    """
    tasks_meta_path = r"LCQBench-555.json"
    
    if not os.path.exists(tasks_meta_path):
        print(f"错误: 找不到文件 {tasks_meta_path}")
        return

    with open(tasks_meta_path, 'r', encoding='utf-8') as f:
        tasks_meta_lists = json.load(f)

    # 给每个任务添加索引，用于最后排序
    for idx, task_meta in enumerate(tasks_meta_lists):
        task_meta['_index'] = idx
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # =======================================================
    # 修改逻辑 1: 定义进度文件 (JSONL) 和读取历史进度
    # =======================================================
    progress_file = os.path.join(output_dir, f"generated_dataset_{lang}_progress.jsonl")
    completed_ids = set()
    
    # 内存中也存一份结果，方便最后快速排序（不用重新读文件）
    # 但为了稳健，最好是最后统一整合
    
    if os.path.exists(progress_file):
        print(f"发现进度文件: {progress_file}，正在恢复进度...")
        with open(progress_file, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line:
                    try:
                        data = json.loads(line)
                        # 使用 problem_id 防止重复
                        completed_ids.add(str(data['problem_id']))
                    except json.JSONDecodeError:
                        continue
        print(f"已恢复 {len(completed_ids)} 个任务，将跳过这些任务。")

    # =======================================================
    # 修改逻辑 2: 过滤待处理任务
    # =======================================================
    tasks_to_do = [
        t for t in tasks_meta_lists 
        if str(t['id']) not in completed_ids
    ]

    total_tasks = len(tasks_meta_lists)
    current_done_count = len(completed_ids)
    remaining_count = len(tasks_to_do)

    # 变量初始化
    failed_tasks = []
    retry_count = 0
    lock = threading.Lock()
    start_time = time.time()
    
    print(f"=" * 60)
    print(f"开始生成代码 (Model: glm-5.2)")
    print(f"总任务: {total_tasks} | 已完成: {current_done_count} | 剩余: {remaining_count}")
    print(f"并发数: {max_workers} | 结果将实时写入: {progress_file}")
    print(f"=" * 60)

    # 如果没有任务要做，直接进入最后合并阶段
    if remaining_count == 0:
        print("所有任务已完成！准备生成最终合并文件。")

    # 进度更新函数
    def update_progress(task_name="", is_retry=False):
        nonlocal current_done_count, retry_count
        with lock:
            if not is_retry:
                current_done_count += 1
            else:
                retry_count += 1
            
            # 计算剩余时间 (只基于本次运行的速度)
            elapsed = time.time() - start_time
            done_in_session = current_done_count - len(completed_ids)
            
            if done_in_session > 0:
                avg_time = elapsed / done_in_session
                remain_seconds = avg_time * (total_tasks - current_done_count)
            else:
                remain_seconds = 0
            
            percent = (current_done_count / total_tasks) * 100
            bar_len = 30
            filled = int(bar_len * current_done_count // total_tasks)
            bar = '█' * filled + '░' * (bar_len - filled)
            
            retry_msg = f" [Retry:{retry_count}]" if retry_count > 0 else ""
            
            # \r 刷新打印
            print(f"\r进度: [{bar}] {percent:.1f}% ({current_done_count}/{total_tasks}){retry_msg} | "
                  f"剩余: {format_time(remain_seconds)} | {task_name[:15]}...", end='', flush=True)

    # =======================================================
    # 修改逻辑 3: 执行线程池 (只处理 tasks_to_do)
    # =======================================================
    if remaining_count > 0:
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_to_task = {
                executor.submit(process_single_task, task_meta, output_dir, lang, max_retries): task_meta
                for task_meta in tasks_to_do
            }
            
            for future in as_completed(future_to_task):
                result = future.result()
                
                if result["success"]:
                    update_progress(result["task_name"])
                    
                    # --- 核心：实时写入文件 ---
                    with lock:
                        # 立即以 JSONL 格式追加写入文件
                        with open(progress_file, 'a', encoding='utf-8') as f:
                            f.write(json.dumps(result["data"], ensure_ascii=False) + "\n")
                            f.flush() # 强制写入硬盘
                else:
                    with lock:
                        failed_tasks.append(result)
                    update_progress(result["task_name"])
                    print(f"\n⚠ 任务失败: {result['task_id']}-{result['task_name']} - {result['error']}")

    # =======================================================
    # 修改逻辑 4: 最终整合结果
    # 读取 progress_file 中的所有数据，并按原始 tasks_meta_lists 顺序排列
    # =======================================================
    print(f"\n\n正在整合最终结果文件...")
    
    # 读取所有已完成的结果（包括以前的和刚刚跑完的）
    all_results_map = {}
    if os.path.exists(progress_file):
        with open(progress_file, 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip():
                    try:
                        data = json.loads(line)
                        all_results_map[str(data['problem_id'])] = data
                    except:
                        pass
    
    # 按原始顺序重组
    final_json_results = []
    for task in tasks_meta_lists:
        tid = str(task['id'])
        if tid in all_results_map:
            final_json_results.append(all_results_map[tid])
    
    # 保存最终 JSON
    json_output_file = os.path.join(output_dir, f"generated_dataset_{lang}.json")
    with open(json_output_file, 'w', encoding='utf-8') as f:
        json.dump(final_json_results, f, ensure_ascii=False, indent=2)
    
    # 显示完成总结
    total_time = time.time() - start_time
    print(f"\n" + "=" * 60)
    print(f"✓ 任务处理完毕！")
    print(f"  - 总数据集: {total_tasks}")
    print(f"  - 最终成功收集: {len(final_json_results)}")
    if failed_tasks:
        print(f"  - 本次失败: {len(failed_tasks)}")
    print(f"  - 本次耗时: {format_time(total_time)}")
    print(f"=" * 60)
    print(f"所有代码文件已保存到: {output_dir}")
    print(f"JSON 格式数据集已保存到: {json_output_file}")
    print(f"过程记录文件(JSONL)保留在: {progress_file}")


if __name__ == "__main__":
    output_directory = ""
    
    # 参数说明:
    # max_workers: 对应原来的配置，50线程
    generate_code(output_directory, lang="python", max_workers=5, max_retries=3)