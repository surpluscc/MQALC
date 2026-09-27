"""
生成性能测试报告
"""

import json
import csv
from datetime import datetime


def load_results(file_path: str):
    """加载测试结果"""
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def generate_summary_report(results):
    """生成摘要报告"""
    print("=" * 100)
    print(" " * 35 + "性能测试摘要报告")
    print("=" * 100)
    print()
    
    # 基本统计
    total = len(results)
    successful = [r for r in results if r.get('success', False)]
    failed = [r for r in results if not r.get('success', False)]
    
    print(f"测试总数: {total}")
    print(f"  成功: {len(successful)} ({len(successful)/total*100:.1f}%)")
    print(f"  失败: {len(failed)} ({len(failed)/total*100:.1f}%)")
    print()
    
    if successful:
        # 时间统计
        times = [r['execution_time_ms'] for r in successful]
        avg_time = sum(times) / len(times)
        min_time = min(times)
        max_time = max(times)
        
        print("运行时间统计 (毫秒):")
        print(f"  平均: {avg_time:.4f} ms")
        print(f"  最小: {min_time:.4f} ms")
        print(f"  最大: {max_time:.4f} ms")
        print()
        
        # 内存统计
        memories = [r['peak_memory_mb'] for r in successful]
        avg_memory = sum(memories) / len(memories)
        min_memory = min(memories)
        max_memory = max(memories)
        
        print("内存使用统计 (MB):")
        print(f"  平均峰值: {avg_memory:.6f} MB")
        print(f"  最小峰值: {min_memory:.6f} MB")
        print(f"  最大峰值: {max_memory:.6f} MB")
        print()
        
        # 按难度分组
        by_difficulty = {}
        for r in results:
            diff = r.get('difficulty', 'Unknown')
            if diff not in by_difficulty:
                by_difficulty[diff] = {'total': 0, 'success': 0, 'times': [], 'memories': []}
            by_difficulty[diff]['total'] += 1
            if r.get('success', False):
                by_difficulty[diff]['success'] += 1
                by_difficulty[diff]['times'].append(r['execution_time_ms'])
                by_difficulty[diff]['memories'].append(r['peak_memory_mb'])
        
        print("按难度统计:")
        print(f"  {'难度':<10} {'成功率':<15} {'平均时间(ms)':<20} {'平均内存(MB)':<20}")
        print("  " + "-" * 75)
        for diff in ['Easy', 'Medium', 'Hard']:
            if diff in by_difficulty:
                stats = by_difficulty[diff]
                success_rate = stats['success'] / stats['total'] * 100 if stats['total'] > 0 else 0
                avg_time = sum(stats['times']) / len(stats['times']) if stats['times'] else 0
                avg_mem = sum(stats['memories']) / len(stats['memories']) if stats['memories'] else 0
                print(f"  {diff:<10} {stats['success']}/{stats['total']} ({success_rate:.1f}%){' '*3} {avg_time:<20.4f} {avg_mem:<20.6f}")
        print()
    
    # 失败的测试
    if failed:
        print("失败的测试:")
        for r in failed:
            print(f"  - {r['problem_title']} ({r['problem_slug']})")
            print(f"    错误: {r.get('error', '未知错误')}")
        print()
    
    print("=" * 100)
    print()


def generate_detailed_report(results, output_file='performance_report_detailed.txt'):
    """生成详细报告"""
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("=" * 100 + "\n")
        f.write(" " * 35 + "详细性能测试报告\n")
        f.write("=" * 100 + "\n\n")
        f.write(f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        
        # 按难度分组
        by_difficulty = {'Easy': [], 'Medium': [], 'Hard': []}
        for r in results:
            diff = r.get('difficulty', 'Unknown')
            if diff in by_difficulty:
                by_difficulty[diff].append(r)
        
        for diff in ['Easy', 'Medium', 'Hard']:
            if by_difficulty[diff]:
                f.write(f"\n{'=' * 100}\n")
                f.write(f"{diff} 难度题目\n")
                f.write(f"{'=' * 100}\n\n")
                
                for r in by_difficulty[diff]:
                    f.write(f"题目: {r['problem_title']} ({r['problem_slug']})\n")
                    f.write(f"题目ID: {r['problem_id']}\n")
                    f.write(f"状态: {'成功' if r.get('success', False) else '失败'}\n")
                    
                    if r.get('success', False):
                        f.write(f"运行时间: {r['execution_time_ms']:.4f} ms ({r['execution_time']:.9f} 秒)\n")
                        f.write(f"峰值内存: {r['peak_memory_mb']:.6f} MB ({r['peak_memory_kb']:.2f} KB)\n")
                        f.write(f"当前内存: {r['current_memory_bytes']} bytes\n")
                        f.write(f"执行结果: {r.get('result', 'N/A')}\n")
                        f.write(f"期望结果: {r.get('expected', 'N/A')}\n")
                    else:
                        f.write(f"错误信息: {r.get('error', '未知错误')}\n")
                        if 'error_type' in r:
                            f.write(f"错误类型: {r['error_type']}\n")
                    
                    f.write("\n" + "-" * 100 + "\n\n")
    
    print(f"详细报告已保存到: {output_file}")


def generate_csv_report(results, output_file='performance_report.csv'):
    """生成CSV报告"""
    with open(output_file, 'w', newline='', encoding='utf-8-sig') as f:
        fieldnames = [
            '题目ID', '题目名称', '题目标识', '难度', '状态',
            '运行时间(ms)', '运行时间(秒)', 
            '峰值内存(MB)', '峰值内存(KB)', '峰值内存(Bytes)',
            '当前内存(Bytes)', '执行结果', '期望结果', '错误信息'
        ]
        
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        
        for r in results:
            row = {
                '题目ID': r['problem_id'],
                '题目名称': r['problem_title'],
                '题目标识': r['problem_slug'],
                '难度': r['difficulty'],
                '状态': '成功' if r.get('success', False) else '失败'
            }
            
            if r.get('success', False):
                row.update({
                    '运行时间(ms)': f"{r['execution_time_ms']:.6f}",
                    '运行时间(秒)': f"{r['execution_time']:.9f}",
                    '峰值内存(MB)': f"{r['peak_memory_mb']:.6f}",
                    '峰值内存(KB)': f"{r['peak_memory_kb']:.2f}",
                    '峰值内存(Bytes)': r['peak_memory_bytes'],
                    '当前内存(Bytes)': r['current_memory_bytes'],
                    '执行结果': r.get('result', ''),
                    '期望结果': r.get('expected', ''),
                    '错误信息': ''
                })
            else:
                row.update({
                    '运行时间(ms)': '',
                    '运行时间(秒)': '',
                    '峰值内存(MB)': '',
                    '峰值内存(KB)': '',
                    '峰值内存(Bytes)': '',
                    '当前内存(Bytes)': '',
                    '执行结果': '',
                    '期望结果': '',
                    '错误信息': r.get('error', '未知错误')
                })
            
            writer.writerow(row)
    
    print(f"CSV报告已保存到: {output_file}")


def generate_markdown_report(results, output_file='performance_report.md'):
    """生成Markdown报告"""
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("# 代码性能测试报告\n\n")
        f.write(f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        
        # 摘要统计
        total = len(results)
        successful = [r for r in results if r.get('success', False)]
        failed = [r for r in results if not r.get('success', False)]
        
        f.write("## 总体统计\n\n")
        f.write(f"- **测试总数**: {total}\n")
        f.write(f"- **成功**: {len(successful)} ({len(successful)/total*100:.1f}%)\n")
        f.write(f"- **失败**: {len(failed)} ({len(failed)/total*100:.1f}%)\n\n")
        
        if successful:
            times = [r['execution_time_ms'] for r in successful]
            memories = [r['peak_memory_mb'] for r in successful]
            
            f.write("## 性能指标\n\n")
            f.write("### 运行时间 (毫秒)\n\n")
            f.write(f"- 平均: {sum(times)/len(times):.4f} ms\n")
            f.write(f"- 最小: {min(times):.4f} ms\n")
            f.write(f"- 最大: {max(times):.4f} ms\n\n")
            
            f.write("### 内存使用 (MB)\n\n")
            f.write(f"- 平均峰值: {sum(memories)/len(memories):.6f} MB\n")
            f.write(f"- 最小峰值: {min(memories):.6f} MB\n")
            f.write(f"- 最大峰值: {max(memories):.6f} MB\n\n")
        
        # 详细测试结果表格
        f.write("## 详细测试结果\n\n")
        f.write("| 题目 | 难度 | 状态 | 运行时间(ms) | 峰值内存(MB) |\n")
        f.write("|------|------|------|--------------|-------------|\n")
        
        for r in results:
            title = r['problem_title']
            diff = r['difficulty']
            status = '✓ 成功' if r.get('success', False) else '✗ 失败'
            
            if r.get('success', False):
                time_str = f"{r['execution_time_ms']:.4f}"
                mem_str = f"{r['peak_memory_mb']:.6f}"
            else:
                time_str = "N/A"
                mem_str = "N/A"
            
            f.write(f"| {title} | {diff} | {status} | {time_str} | {mem_str} |\n")
        
        f.write("\n")
        
        # 失败的测试
        if failed:
            f.write("## 失败的测试\n\n")
            for r in failed:
                f.write(f"### {r['problem_title']} ({r['problem_slug']})\n\n")
                f.write(f"- **错误**: {r.get('error', '未知错误')}\n")
                if 'error_type' in r:
                    f.write(f"- **错误类型**: {r['error_type']}\n")
                f.write("\n")
    
    print(f"Markdown报告已保存到: {output_file}")


def main():
    """主函数"""
    print("正在生成报告...\n")
    
    # 加载结果
    results = load_results('performance_results.json')
    
    # 生成各种报告
    generate_summary_report(results)
    generate_detailed_report(results)
    generate_csv_report(results)
    generate_markdown_report(results)
    
    print("\n所有报告生成完成!")


if __name__ == '__main__':
    main()

