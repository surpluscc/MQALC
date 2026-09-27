"""
批量分析Python代码的可维护性指数(MI)
生成详细报告文件
"""
import os
import sys
from datetime import datetime

# 检查radon是否已安装
try:
    from radon.metrics import mi_visit, mi_rank
except ImportError:
    print("错误: 未安装radon库")
    print("请先安装: pip install radon")
    sys.exit(1)


def analyze_directory(directory_path, output_file="mi_report.txt"):
    """
    分析指定目录下的所有Python文件
    
    参数:
        directory_path: 要分析的目录路径
        output_file: 报告文件名
    """
    print(f"正在扫描目录: {directory_path}")
    
    # 收集所有Python文件
    python_files = []
    for root, dirs, files in os.walk(directory_path):
        for file in files:
            if file.endswith('.py'):
                python_files.append(os.path.join(root, file))
    
    if not python_files:
        print("错误: 未找到Python文件")
        return
    
    print(f"找到 {len(python_files)} 个Python文件")
    print("正在分析...")
    
    # 分析每个文件
    results = []
    for py_file in python_files:
        try:
            # 读取文件内容
            with open(py_file, 'r', encoding='utf-8') as f:
                source_code = f.read()
            
            # 计算MI值
            mi_score = mi_visit(source_code, multi=True)
            rank = mi_rank(mi_score)
            
            # 获取相对路径（更易读）
            rel_path = os.path.relpath(py_file, directory_path)
            results.append({
                'file': rel_path,
                'full_path': py_file,
                'mi': mi_score,
                'rank': rank
            })
        except Exception as e:
            print(f"  警告: 分析 {py_file} 时出错 - {str(e)}")
    
    if not results:
        print("错误: 没有成功分析的文件")
        return
    
    # 按文件ID（文件名开头的数字）排序
    def extract_id(filename):
        """从文件名中提取开头的数字ID"""
        import re
        match = re.match(r'(\d+)', filename)
        return int(match.group(1)) if match else 0
    
    results.sort(key=lambda x: extract_id(x['file']))
    
    # 计算统计数据
    total_mi = sum(r['mi'] for r in results)
    avg_mi = total_mi / len(results)
    max_mi = max(r['mi'] for r in results)
    min_mi = min(r['mi'] for r in results)
    
    # 统计各等级数量
    rank_count = {'A': 0, 'B': 0, 'C': 0}
    for r in results:
        rank_count[r['rank']] = rank_count.get(r['rank'], 0) + 1
    
    # 生成报告
    generate_report(results, avg_mi, max_mi, min_mi, rank_count, 
                   directory_path, output_file)
    
    # 终端输出最终结果
    print("\n" + "=" * 70)
    print("分析完成！")
    print("=" * 70)
    print(f"\n总文件数: {len(results)}")
    print(f"平均MI值: {avg_mi:.2f}")
    print(f"最高MI值: {max_mi:.2f}")
    print(f"最低MI值: {min_mi:.2f}")
    print(f"\n等级分布:")
    print(f"  A级 (优秀): {rank_count['A']} 个文件")
    print(f"  B级 (中等): {rank_count['B']} 个文件")
    print(f"  C级 (较差): {rank_count['C']} 个文件")
    print(f"\n详细报告已保存到: {output_file}")
    print("=" * 70)


def generate_report(results, avg_mi, max_mi, min_mi, rank_count, 
                   directory, output_file):
    """生成详细报告文件"""
    with open(output_file, 'w', encoding='utf-8') as f:
        # 报告头部
        f.write("=" * 80 + "\n")
        f.write("代码可维护性指数(MI)分析报告\n")
        f.write("=" * 80 + "\n\n")
        
        f.write(f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"分析目录: {directory}\n")
        f.write(f"文件总数: {len(results)}\n\n")
        
        # 统计摘要
        f.write("-" * 80 + "\n")
        f.write("统计摘要\n")
        f.write("-" * 80 + "\n\n")
        
        f.write(f"平均MI值: {avg_mi:.2f}\n")
        f.write(f"最高MI值: {max_mi:.2f}\n")
        f.write(f"最低MI值: {min_mi:.2f}\n\n")
        
        f.write("等级分布:\n")
        f.write(f"  A级 (20-100, 优秀): {rank_count['A']} 个文件 ({rank_count['A']/len(results)*100:.1f}%)\n")
        f.write(f"  B级 (10-19,  中等): {rank_count['B']} 个文件 ({rank_count['B']/len(results)*100:.1f}%)\n")
        f.write(f"  C级 (0-9,    较差): {rank_count['C']} 个文件 ({rank_count['C']/len(results)*100:.1f}%)\n\n")
        
        # 详细列表
        f.write("-" * 80 + "\n")
        f.write("所有文件详细分析结果（按文件ID顺序排列）\n")
        f.write("-" * 80 + "\n\n")
        
        for i, result in enumerate(results, 1):
            f.write(f"{i}. {result['file']}\n")
            f.write(f"   MI值: {result['mi']:.2f}  |  等级: {result['rank']}")
            
            # 添加等级说明
            if result['rank'] == 'A':
                f.write("  ✓ 优秀\n")
            elif result['rank'] == 'B':
                f.write("  ⚠ 中等\n")
            else:
                f.write("  ✗ 较差\n")
            f.write("\n")
        
        # 分类列表
        f.write("-" * 80 + "\n")
        f.write("按等级分类\n")
        f.write("-" * 80 + "\n\n")
        
        for rank_level in ['A', 'B', 'C']:
            rank_name = {'A': '优秀', 'B': '中等', 'C': '较差'}[rank_level]
            f.write(f"\n{rank_level}级文件 ({rank_name}):\n")
            f.write("-" * 40 + "\n")
            
            rank_files = [r for r in results if r['rank'] == rank_level]
            if rank_files:
                for result in rank_files:
                    f.write(f"  • {result['file']} (MI: {result['mi']:.2f})\n")
            else:
                f.write("  无\n")
        
        # 需要改进的文件
        f.write("\n" + "-" * 80 + "\n")
        f.write("重点关注（MI值低于20的文件）\n")
        f.write("-" * 80 + "\n\n")
        
        low_mi_files = [r for r in results if r['mi'] < 20]
        if low_mi_files:
            for result in low_mi_files:
                f.write(f"• {result['file']}\n")
                f.write(f"  MI值: {result['mi']:.2f}  |  等级: {result['rank']}\n")
                
                if result['mi'] < 10:
                    f.write("  建议: 强烈建议重构\n")
                    f.write("    - 拆分复杂函数\n")
                    f.write("    - 减少嵌套层级\n")
                    f.write("    - 增加注释\n")
                else:
                    f.write("  建议: 考虑优化\n")
                    f.write("    - 重构部分复杂代码\n")
                    f.write("    - 增加注释\n")
                f.write("\n")
        else:
            f.write("所有文件MI值均>=20，代码质量良好！\n")
        
        # 报告尾部
        f.write("\n" + "=" * 80 + "\n")
        f.write("说明:\n")
        f.write("  MI (Maintainability Index) - 可维护性指数\n")
        f.write("  取值范围: 0-100\n")
        f.write("  A级 (20-100): 代码结构清晰，易于维护\n")
        f.write("  B级 (10-19):  代码可维护性中等，建议优化\n")
        f.write("  C级 (0-9):    代码可维护性较差，需要重构\n")
        f.write("=" * 80 + "\n")


def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("使用方法: python batch_analyze.py <目录路径> [报告文件名]")
        print("\n示例:")
        print('  python batch_analyze.py ""')
        print('  python batch_analyze.py "" report.txt')
        sys.exit(1)
    
    directory = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else "mi_report.txt"
    
    # 检查目录是否存在
    if not os.path.exists(directory):
        print(f"错误: 目录不存在 - {directory}")
        sys.exit(1)
    
    if not os.path.isdir(directory):
        print(f"错误: 不是目录 - {directory}")
        sys.exit(1)
    
    # 执行分析
    analyze_directory(directory, output_file)


if __name__ == "__main__":
    main()

