"""
代码性能测试脚本
测试 generate_code_passed.json 中代码的运行时间和内存占用
"""

import json
import time
import tracemalloc
import sys
import io
import os
from typing import Dict, List, Any, Optional
import subprocess
import tempfile
import re

# 设置输出编码，避免 Windows 系统的编码问题
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'ignore')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'ignore')


def load_generated_code(file_path: str) -> List[Dict]:
    """加载生成的代码"""
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def load_dataset(file_path: str) -> Dict[str, Dict]:
    """加载数据集并按 task_id 索引"""
    dataset = {}
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip():
                data = json.loads(line)
                dataset[data['task_id']] = data
    return dataset


def extract_first_test_case(test_cases: List[Dict]) -> Optional[Dict]:
    """提取第一个测试用例"""
    if test_cases and len(test_cases) > 0:
        return test_cases[0]
    return None


def parse_input_string(input_str: str) -> Dict[str, Any]:
    """解析输入字符串,提取参数"""
    # 移除多余的空白
    input_str = input_str.strip()
    
    # 提取所有参数
    params = {}
    
    # 使用正则表达式匹配参数
    # 匹配形如 "param_name = value" 的模式
    pattern = r'(\w+)\s*=\s*(.+?)(?=,\s*\w+\s*=|$)'
    matches = re.findall(pattern, input_str)
    
    for param_name, param_value in matches:
        param_value = param_value.strip()
        # 尝试用 eval 解析值(在安全的上下文中)
        try:
            params[param_name] = eval(param_value)
        except:
            params[param_name] = param_value
    
    return params


def create_test_code(code: str, test_case: Dict, problem_slug: str, dataset_info: Dict) -> str:
    """创建完整的测试代码"""
    
    # 获取输入输出
    input_str = test_case.get('input', '')
    expected_output = test_case.get('output', None)
    
    # 解析输入参数
    params = parse_input_string(input_str)
    
    # 准备导入语句
    imports = """
import sys
import time
import tracemalloc
from typing import *
from functools import *
from collections import *
from itertools import *
from heapq import *
from bisect import *
from string import *
from operator import *
from math import *
from queue import Queue

# ListNode 定义
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

def list_node(values: list):
    if not values:
        return None
    head = ListNode(values[0])
    p = head
    for val in values[1:]:
        node = ListNode(val)
        p.next = node
        p = node
    return head

def is_same_list(p1, p2):
    if p1 is None and p2 is None:
        return True
    if not p1 or not p2:
        return False
    return p1.val == p2.val and is_same_list(p1.next, p2.next)

# TreeNode 定义
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def tree_node(values: list):
    if not values:
        return None
    root = TreeNode(values[0])
    i = 1
    queue = deque()
    queue.append(root)
    while queue:
        node = queue.popleft()
        if i < len(values) and values[i] is not None:
            node.left = TreeNode(values[i])
            queue.append(node.left)
        i += 1
        if i < len(values) and values[i] is not None:
            node.right = TreeNode(values[i])
            queue.append(node.right)
        i += 1
    return root

def is_same_tree(p, q):
    if not p and not q:
        return True
    elif not p or not q:
        return False
    elif p.val != q.val:
        return False
    else:
        return is_same_tree(p.left, q.left) and is_same_tree(p.right, q.right)
"""
    
    # 清理代码,移除可能的测试代码
    clean_code = code
    # 移除包含 "# Test" 或 "print" 的行
    lines = clean_code.split('\n')
    filtered_lines = []
    in_solution_class = False
    for line in lines:
        # 如果遇到 class Solution,开始记录
        if 'class Solution' in line:
            in_solution_class = True
        
        # 跳过测试相关的代码
        if '# Test' in line or (line.strip().startswith('print(') and 'solution' in line.lower()):
            continue
        
        # 如果已经结束了 Solution 类定义,并且遇到了新的代码块,停止
        if in_solution_class and line and not line[0].isspace() and 'class Solution' not in line:
            # 检查是否是导入语句或注释
            if not line.startswith('from ') and not line.startswith('import ') and not line.startswith('#'):
                break
        
        filtered_lines.append(line)
    
    clean_code = '\n'.join(filtered_lines)
    
    # 构建参数字符串
    param_str = ', '.join([f'{k}={repr(v)}' for k, v in params.items()])
    
    # 获取方法名 (从 starter_code 或通过其他方式)
    method_name = None
    if dataset_info:
        starter_code = dataset_info.get('starter_code', '')
        # 从 starter_code 中提取方法名
        import re
        match = re.search(r'def\s+(\w+)\s*\(', starter_code)
        if match:
            method_name = match.group(1)
    
    if not method_name:
        # 尝试从代码中提取
        match = re.search(r'def\s+(\w+)\s*\(', clean_code)
        if match:
            method_name = match.group(1)
        else:
            method_name = 'solution'
    
    # 创建完整代码
    full_code = f"""{imports}

{clean_code}

if __name__ == "__main__":
    # 初始化
    solution = Solution()
    
    # 准备测试数据
    test_input = {repr(params)}
    
    # 开始内存跟踪
    tracemalloc.start()
    
    # 记录开始时间
    start_time = time.perf_counter()
    
    # 执行代码
    try:
        result = solution.{method_name}(**test_input)
        
        # 记录结束时间
        end_time = time.perf_counter()
        
        # 获取内存使用情况
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        
        # 计算执行时间(秒)
        execution_time = end_time - start_time
        
        # 输出结果(JSON格式,便于解析)
        import json
        output = {{
            "success": True,
            "execution_time": execution_time,
            "execution_time_ms": execution_time * 1000,
            "peak_memory_bytes": peak,
            "peak_memory_kb": peak / 1024,
            "peak_memory_mb": peak / (1024 * 1024),
            "current_memory_bytes": current,
            "result": str(result),
            "expected": {repr(expected_output)}
        }}
        print("===RESULT_START===")
        print(json.dumps(output, ensure_ascii=False))
        print("===RESULT_END===")
        
    except Exception as e:
        tracemalloc.stop()
        import json
        output = {{
            "success": False,
            "error": str(e),
            "error_type": type(e).__name__,
            "traceback": traceback.format_exc()
        }}
        print("===RESULT_START===")
        print(json.dumps(output, ensure_ascii=False))
        print("===RESULT_END===")
"""
    
    return full_code


def run_code_in_sandbox(code: str, timeout: int = 30) -> Dict:
    """在沙箱环境中运行代码"""
    
    # 创建临时文件
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False, encoding='utf-8') as f:
        f.write(code)
        temp_file = f.name
    
    try:
        # 使用 subprocess 运行代码,限制资源
        result = subprocess.run(
            [sys.executable, temp_file],
            capture_output=True,
            text=True,
            timeout=timeout,
            encoding='utf-8'
        )
        
        # 解析输出
        output = result.stdout
        
        # 查找结果
        if '===RESULT_START===' in output and '===RESULT_END===' in output:
            start_idx = output.index('===RESULT_START===') + len('===RESULT_START===')
            end_idx = output.index('===RESULT_END===')
            result_json = output[start_idx:end_idx].strip()
            
            return json.loads(result_json)
        else:
            return {
                'success': False,
                'error': '无法解析输出',
                'stdout': output,
                'stderr': result.stderr
            }
    
    except subprocess.TimeoutExpired:
        return {
            'success': False,
            'error': '执行超时',
            'timeout': timeout
        }
    except Exception as e:
        return {
            'success': False,
            'error': str(e),
            'error_type': type(e).__name__
        }
    finally:
        # 删除临时文件
        try:
            os.unlink(temp_file)
        except:
            pass


def main():
    """主函数"""
    
    print("=" * 80)
    print("代码性能测试")
    print("=" * 80)
    print()
    
    # 加载生成的代码
    print("正在加载生成的代码...")
    generated_codes = load_generated_code('generate_code_passed.json')
    print(f"已加载 {len(generated_codes)} 个代码样本")
    print()
    
    # 选择最新版本的数据集
    dataset_files = [
        'data/LeetCodeDataset.jsonl',
    ]
    
    dataset = None
    for dataset_file in dataset_files:
        if os.path.exists(dataset_file):
            print(f"正在加载数据集: {dataset_file}")
            dataset = load_dataset(dataset_file)
            print(f"已加载 {len(dataset)} 个题目")
            break
    
    if not dataset:
        print("错误: 未找到数据集文件")
        return
    
    print()
    print("-" * 80)
    print()
    
    # 存储所有测试结果
    all_results = []
    
    # 对每个代码样本进行测试
    for idx, code_info in enumerate(generated_codes, 1):
        problem_id = code_info['problem_id']
        problem_slug = code_info['problem_slug']
        difficulty = code_info['difficulty']
        code = code_info['generated_code']
        
        # 查找对应的数据集信息
        dataset_info = dataset.get(problem_slug)
        
        # 尝试从数据集获取 problem_title，否则使用 problem_slug
        if dataset_info:
            problem_title = dataset_info.get('problem_description', '').split('\n')[0][:50] if dataset_info.get('problem_description') else problem_slug
            if not problem_title.strip():
                problem_title = problem_slug
            # 清理特殊字符，避免编码问题
            problem_title = problem_title.replace('\xa0', ' ').replace('\u200b', '').strip()
        else:
            problem_title = code_info.get('problem_title', problem_slug)
        
        print(f"[{idx}/{len(generated_codes)}] 测试题目: {problem_title} ({problem_slug})")
        print(f"  难度: {difficulty}")
        print(f"  题目ID: {problem_id}")
        
        if not dataset_info:
            print(f"  [警告] 未找到对应的数据集信息")
            all_results.append({
                'problem_id': problem_id,
                'problem_slug': problem_slug,
                'problem_title': problem_title,
                'difficulty': difficulty,
                'success': False,
                'error': '未找到对应的数据集信息'
            })
            print()
            continue
        
        # 提取第一个测试用例
        test_cases = dataset_info.get('input_output', [])
        if not test_cases:
            print(f"  [警告] 没有可用的测试用例")
            all_results.append({
                'problem_id': problem_id,
                'problem_slug': problem_slug,
                'problem_title': problem_title,
                'difficulty': difficulty,
                'success': False,
                'error': '没有可用的测试用例'
            })
            print()
            continue
        
        first_test_case = test_cases[0]
        print(f"  测试用例: {first_test_case['input'][:80]}...")
        
        # 创建测试代码
        try:
            test_code = create_test_code(code, first_test_case, problem_slug, dataset_info)
        except Exception as e:
            print(f"  [失败] 创建测试代码失败: {e}")
            all_results.append({
                'problem_id': problem_id,
                'problem_slug': problem_slug,
                'problem_title': problem_title,
                'difficulty': difficulty,
                'success': False,
                'error': f'创建测试代码失败: {e}'
            })
            print()
            continue
        
        # 在沙箱中运行
        print("  正在运行测试...")
        result = run_code_in_sandbox(test_code, timeout=30)
        
        # 记录结果
        result_entry = {
            'problem_id': problem_id,
            'problem_slug': problem_slug,
            'problem_title': problem_title,
            'difficulty': difficulty,
            **result
        }
        all_results.append(result_entry)
        
        # 显示结果
        if result['success']:
            print(f"  [成功] 执行成功")
            print(f"    运行时间: {result['execution_time_ms']:.3f} ms")
            print(f"    峰值内存: {result['peak_memory_kb']:.2f} KB ({result['peak_memory_mb']:.4f} MB)")
        else:
            print(f"  [失败] 执行失败: {result.get('error', '未知错误')}")
        
        print()
    
    # 保存结果
    print("-" * 80)
    print()
    print("正在保存结果...")
    
    output_file = 'performance_results.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(all_results, f, ensure_ascii=False, indent=2)
    
    print(f"结果已保存到: {output_file}")
    print()
    
    # 统计汇总
    print("=" * 80)
    print("测试汇总")
    print("=" * 80)
    print()
    
    total = len(all_results)
    successful = sum(1 for r in all_results if r.get('success', False))
    failed = total - successful
    
    print(f"总测试数: {total}")
    print(f"成功: {successful} ({successful/total*100:.1f}%)")
    print(f"失败: {failed} ({failed/total*100:.1f}%)")
    print()
    
    # 成功的测试统计
    if successful > 0:
        successful_results = [r for r in all_results if r.get('success', False)]
        
        avg_time = sum(r['execution_time_ms'] for r in successful_results) / successful
        avg_memory = sum(r['peak_memory_mb'] for r in successful_results) / successful
        
        max_time_result = max(successful_results, key=lambda r: r['execution_time_ms'])
        min_time_result = min(successful_results, key=lambda r: r['execution_time_ms'])
        
        max_memory_result = max(successful_results, key=lambda r: r['peak_memory_mb'])
        min_memory_result = min(successful_results, key=lambda r: r['peak_memory_mb'])
        
        print("性能统计 (成功的测试):")
        print(f"  平均运行时间: {avg_time:.3f} ms")
        print(f"  平均峰值内存: {avg_memory:.4f} MB")
        print()
        print(f"  最快: {min_time_result['problem_title']} - {min_time_result['execution_time_ms']:.3f} ms")
        print(f"  最慢: {max_time_result['problem_title']} - {max_time_result['execution_time_ms']:.3f} ms")
        print()
        print(f"  最少内存: {min_memory_result['problem_title']} - {min_memory_result['peak_memory_mb']:.4f} MB")
        print(f"  最多内存: {max_memory_result['problem_title']} - {max_memory_result['peak_memory_mb']:.4f} MB")
        print()
    
    # 按难度统计
    difficulties = {}
    for r in all_results:
        diff = r.get('difficulty', 'Unknown')
        if diff not in difficulties:
            difficulties[diff] = {'total': 0, 'success': 0}
        difficulties[diff]['total'] += 1
        if r.get('success', False):
            difficulties[diff]['success'] += 1
    
    print("按难度统计:")
    for diff, stats in sorted(difficulties.items()):
        success_rate = stats['success'] / stats['total'] * 100 if stats['total'] > 0 else 0
        print(f"  {diff}: {stats['success']}/{stats['total']} ({success_rate:.1f}%)")
    
    print()
    print("=" * 80)
    print("测试完成!")
    print("=" * 80)


if __name__ == '__main__':
    main()

