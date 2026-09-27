"""
生成详细的性能统计报告
"""

import json
from collections import defaultdict
from datetime import datetime

def load_json(file_path):
    """加载JSON文件"""
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def generate_statistics_report():
    """生成统计报告"""
    
    # 加载数据
    print("正在加载数据...")
    performance_results = load_json('performance_results.json')
    code_data = load_json('generate_code_passed.json')
    
    # 创建problem_id到estimated_date的映射
    date_mapping = {}
    for item in code_data:
        date_mapping[item['problem_id']] = item.get('estimated_date', 'Unknown')
    
    # 筛选成功的测试结果
    successful_tests = [r for r in performance_results if r.get('success', False)]
    
    print(f"总测试数: {len(performance_results)}")
    print(f"成功测试数: {len(successful_tests)}")
    print()
    
    # 为每个成功的测试添加estimated_date
    for test in successful_tests:
        test['estimated_date'] = date_mapping.get(test['problem_id'], 'Unknown')
    
    # 按难度分组统计
    difficulty_stats = defaultdict(lambda: {'tests': [], 'count': 0})
    for test in successful_tests:
        diff = test['difficulty']
        difficulty_stats[diff]['tests'].append(test)
        difficulty_stats[diff]['count'] += 1
    
    # 按年份分组统计
    year_stats = defaultdict(lambda: {'tests': [], 'count': 0})
    for test in successful_tests:
        date_str = test.get('estimated_date', 'Unknown')
        if date_str and date_str != 'Unknown':
            year = date_str.split('-')[0]  # 提取年份
            year_stats[year]['tests'].append(test)
            year_stats[year]['count'] += 1
    
    # 生成报告
    report_lines = []
    report_lines.append("=" * 100)
    report_lines.append("代码性能测试统计报告")
    report_lines.append("=" * 100)
    report_lines.append("")
    report_lines.append(f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report_lines.append("")
    
    # ==================== 总体统计 ====================
    report_lines.append("-" * 100)
    report_lines.append("一、总体统计")
    report_lines.append("-" * 100)
    report_lines.append("")
    
    total_tests = len(performance_results)
    successful_count = len(successful_tests)
    failed_count = total_tests - successful_count
    
    report_lines.append(f"总测试数量: {total_tests}")
    report_lines.append(f"成功测试数量: {successful_count} ({successful_count/total_tests*100:.1f}%)")
    report_lines.append(f"失败测试数量: {failed_count} ({failed_count/total_tests*100:.1f}%)")
    report_lines.append("")
    
    if successful_tests:
        avg_time_ms = sum(t['execution_time_ms'] for t in successful_tests) / len(successful_tests)
        avg_memory_mb = sum(t['peak_memory_mb'] for t in successful_tests) / len(successful_tests)
        avg_memory_kb = avg_memory_mb * 1024
        
        report_lines.append(f"平均执行时间: {avg_time_ms:.6f} ms")
        report_lines.append(f"平均峰值内存: {avg_memory_mb:.6f} MB ({avg_memory_kb:.4f} KB)")
        report_lines.append("")
        
        # 极值统计
        fastest = min(successful_tests, key=lambda x: x['execution_time_ms'])
        slowest = max(successful_tests, key=lambda x: x['execution_time_ms'])
        min_memory = min(successful_tests, key=lambda x: x['peak_memory_mb'])
        max_memory = max(successful_tests, key=lambda x: x['peak_memory_mb'])
        
        report_lines.append("极值统计:")
        report_lines.append(f"  最快执行时间: {fastest['execution_time_ms']:.6f} ms")
        report_lines.append(f"    题目: {fastest['problem_title'][:60]}...")
        report_lines.append(f"    题目ID: {fastest['problem_id']} ({fastest['problem_slug']})")
        report_lines.append("")
        report_lines.append(f"  最慢执行时间: {slowest['execution_time_ms']:.6f} ms")
        report_lines.append(f"    题目: {slowest['problem_title'][:60]}...")
        report_lines.append(f"    题目ID: {slowest['problem_id']} ({slowest['problem_slug']})")
        report_lines.append("")
        report_lines.append(f"  最少内存占用: {min_memory['peak_memory_mb']:.6f} MB ({min_memory['peak_memory_kb']:.4f} KB)")
        report_lines.append(f"    题目: {min_memory['problem_title'][:60]}...")
        report_lines.append(f"    题目ID: {min_memory['problem_id']} ({min_memory['problem_slug']})")
        report_lines.append("")
        report_lines.append(f"  最多内存占用: {max_memory['peak_memory_mb']:.6f} MB ({max_memory['peak_memory_kb']:.4f} KB)")
        report_lines.append(f"    题目: {max_memory['problem_title'][:60]}...")
        report_lines.append(f"    题目ID: {max_memory['problem_id']} ({max_memory['problem_slug']})")
        report_lines.append("")
    
    # ==================== 按难度统计 ====================
    report_lines.append("-" * 100)
    report_lines.append("二、按难度分组统计")
    report_lines.append("-" * 100)
    report_lines.append("")
    
    for difficulty in ['Easy', 'Medium', 'Hard']:
        if difficulty in difficulty_stats:
            stats = difficulty_stats[difficulty]
            tests = stats['tests']
            count = stats['count']
            
            avg_time = sum(t['execution_time_ms'] for t in tests) / count
            avg_memory_mb = sum(t['peak_memory_mb'] for t in tests) / count
            avg_memory_kb = avg_memory_mb * 1024
            
            report_lines.append(f"【{difficulty}】")
            report_lines.append(f"  题目数量: {count}")
            report_lines.append(f"  平均执行时间: {avg_time:.6f} ms")
            report_lines.append(f"  平均峰值内存: {avg_memory_mb:.6f} MB ({avg_memory_kb:.4f} KB)")
            report_lines.append("")
    
    # ==================== 按年份统计 ====================
    report_lines.append("-" * 100)
    report_lines.append("三、按年份分组统计")
    report_lines.append("-" * 100)
    report_lines.append("")
    
    for year in sorted(year_stats.keys()):
        stats = year_stats[year]
        tests = stats['tests']
        count = stats['count']
        
        if count > 0:
            avg_time = sum(t['execution_time_ms'] for t in tests) / count
            avg_memory_mb = sum(t['peak_memory_mb'] for t in tests) / count
            avg_memory_kb = avg_memory_mb * 1024
            
            report_lines.append(f"【{year}年】")
            report_lines.append(f"  题目数量: {count}")
            report_lines.append(f"  平均执行时间: {avg_time:.6f} ms")
            report_lines.append(f"  平均峰值内存: {avg_memory_mb:.6f} MB ({avg_memory_kb:.4f} KB)")
            report_lines.append("")
    
    # ==================== 通过测试的题目列表 ====================
    report_lines.append("-" * 100)
    report_lines.append("四、通过测试的题目列表")
    report_lines.append("-" * 100)
    report_lines.append("")
    report_lines.append(f"共 {len(successful_tests)} 道题目通过测试:")
    report_lines.append("")
    
    # 按难度分组显示
    for difficulty in ['Easy', 'Medium', 'Hard']:
        if difficulty in difficulty_stats:
            tests = difficulty_stats[difficulty]['tests']
            report_lines.append(f"【{difficulty} - {len(tests)} 题】")
            report_lines.append("")
            
            for idx, test in enumerate(tests, 1):
                report_lines.append(f"  {idx}. {test['problem_title'][:70]}")
                report_lines.append(f"     题目ID: {test['problem_id']} | Slug: {test['problem_slug']}")
                report_lines.append(f"     执行时间: {test['execution_time_ms']:.6f} ms | 内存: {test['peak_memory_mb']:.6f} MB")
                report_lines.append(f"     预估日期: {test.get('estimated_date', 'Unknown')}")
                report_lines.append("")
            
            report_lines.append("")
    
    # ==================== 失败的测试 ====================
    failed_tests = [r for r in performance_results if not r.get('success', False)]
    if failed_tests:
        report_lines.append("-" * 100)
        report_lines.append("五、失败的测试")
        report_lines.append("-" * 100)
        report_lines.append("")
        report_lines.append(f"共 {len(failed_tests)} 道题目测试失败:")
        report_lines.append("")
        
        for idx, test in enumerate(failed_tests, 1):
            report_lines.append(f"{idx}. {test.get('problem_title', test['problem_slug'])[:70]}")
            report_lines.append(f"   题目ID: {test['problem_id']} | Slug: {test['problem_slug']}")
            report_lines.append(f"   难度: {test['difficulty']}")
            report_lines.append(f"   失败原因: {test.get('error', '未知错误')}")
            report_lines.append("")
    
    # ==================== 结束 ====================
    report_lines.append("=" * 100)
    report_lines.append("报告结束")
    report_lines.append("=" * 100)
    
    # 保存报告
    report_content = '\n'.join(report_lines)
    output_file = 'performance_statistics_report.txt'
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(report_content)
    
    print(f"统计报告已生成: {output_file}")
    print(f"报告包含 {len(report_lines)} 行")
    
    return output_file

if __name__ == '__main__':
    generate_statistics_report()

