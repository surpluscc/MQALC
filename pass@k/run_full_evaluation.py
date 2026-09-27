import json
import sys
import os
import time


def print_section(title):
    """打印分节标题"""
    print("\n" + "=" * 70)
    print(title)
    print("=" * 70 + "\n")

def step1_convert_format(input_file):
    """步骤1: 转换文件格式"""
    print_section("步骤 1/5: 转换文件格式")
    
    if not os.path.exists(input_file):
        print(f"错误: 找不到输入文件 {input_file}")
        return False
    
    try:
        # 读取原始 JSON
        with open(input_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        print(f"读取文件: {input_file}")
        print(f"问题数量: {len(data)}")
        
        # 转换为 JSONL
        output_file = input_file.replace('.json', '.jsonl')
        results = []
        
        for item in data:
            converted = {
                'task_id': item['problem_slug'],
                'completion': item['generated_code']
            }
            results.append(converted)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            for item in results:
                f.write(json.dumps(item, ensure_ascii=False) + '\n')
        
        print(f"转换完成: {output_file}")
        return output_file
    
    except Exception as e:
        print(f"转换失败: {e}")
        return False

def step2_check_dataset(jsonl_file):
    """步骤2: 检查数据集匹配"""
    print_section("步骤 2/5: 检查数据集匹配")
    
    from eval_lcd.data import read_jsonl, read_problems, get_problem_file
    
    try:
        # 读取问题数据集
        problem_file = get_problem_file()
        problems = read_problems(problem_file)
        print(f"数据集文件: {os.path.basename(problem_file)}")
        print(f"数据集大小: {len(problems)} 题")
        
        # 读取待测试的问题
        samples = list(read_jsonl(jsonl_file))
        task_ids = [s['task_id'] for s in samples]
        
        # 检查匹配
        matched = [tid for tid in task_ids if tid in problems]
        not_matched = [tid for tid in task_ids if tid not in problems]
        
        print(f"\n待测问题: {len(task_ids)} 题")
        print(f"匹配成功: {len(matched)} 题")
        print(f"未匹配: {len(not_matched)} 题")
        
        if not_matched:
            print(f"\n未匹配的问题:")
            for tid in not_matched[:5]:
                print(f"  - {tid}")
            if len(not_matched) > 5:
                print(f"  ... 还有 {len(not_matched)-5} 个")
        
        if len(matched) == 0:
            print("\n错误: 没有问题匹配，无法继续")
            return False
        
        return True
    
    except Exception as e:
        print(f"检查失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def step3_run_evaluation(jsonl_file, n_workers=4, timeout=10):
    """步骤3: 运行判题（使用 eval_lcd 标准评估）"""
    print_section("步骤 3/5: 运行判题（计算 pass@1）")

    print("使用 eval_lcd 标准评估功能...")
    print(f"并行进程数: {n_workers}, 超时设置: {timeout}秒\n")

    try:
        from eval_lcd.data import get_problem_file
        from eval_lcd.evaluate import evaluate_functional_correctness

        # ----------------------------------------------------------
        # 获取问题数据集
        # ----------------------------------------------------------
        problem_file = get_problem_file()
        
        # ----------------------------------------------------------
        # 使用 eval_lcd 的标准评估功能
        # ----------------------------------------------------------
        # k=[1] 表示只计算 pass@1
        pass_at_k = evaluate_functional_correctness(
            sample_file=jsonl_file,
            problem_file=problem_file,
            k=[1],  # 计算 pass@1
            n_workers=n_workers,
            timeout=timeout
        )

        # 结果文件自动生成为 {jsonl_file}_results.jsonl
        result_file = jsonl_file + "_results.jsonl"
        
        print(f"\n[OK] 结果已保存: {result_file}")
        print(f"[OK] pass@1: {pass_at_k.get('pass@1', 0):.1%}")

        return result_file, pass_at_k

    except Exception as e:
        print(f"\n判题失败: {e}")
        import traceback
        traceback.print_exc()
        return False, None


def step4_generate_report(result_file, original_file, pass_at_k=None):
    """步骤4: 生成报告（增强版：增加难度与年份统计，显示 pass@1）"""
    print_section("步骤 4/5: 生成报告")
    
    try:
        # 读取结果
        results = []
        with open(result_file, 'r', encoding='utf-8') as f:
            for line in f:
                results.append(json.loads(line))
        
        # 读取原始数据（用于难度与日期信息）
        with open(original_file, 'r', encoding='utf-8') as f:
            original_data = json.load(f)
            difficulty_map = {item['problem_slug']: item.get('difficulty', 'Unknown') for item in original_data}
            date_map = {item['problem_slug']: item.get('estimated_date', '') for item in original_data}
        
        # 基础统计
        total = len(results)
        passed = sum(1 for r in results if r['passed'])
        
        # 使用 pass@1 或简单通过率
        if pass_at_k and 'pass@1' in pass_at_k:
            pass_1_value = pass_at_k['pass@1']
            metric_name = "pass@1"
        else:
            pass_1_value = passed / total if total > 0 else 0
            metric_name = "通过率"

        # ------------------------------
        # 📊 统计各难度下通过数量
        # ------------------------------
        passed_by_difficulty = {"Easy": 0, "Medium": 0, "Hard": 0, "Unknown": 0}
        passed_by_year = {"2023": 0, "2024": 0, "其他": 0}

        for r in results:
            if r['passed']:
                slug = r['task_id']
                diff = difficulty_map.get(slug, "Unknown")
                passed_by_difficulty[diff] = passed_by_difficulty.get(diff, 0) + 1

                # 判断年份
                date_str = date_map.get(slug, "")
                if date_str.startswith("2023"):
                    passed_by_year["2023"] += 1
                elif date_str.startswith("2024"):
                    passed_by_year["2024"] += 1
                else:
                    passed_by_year["其他"] += 1

        # ------------------------------
        # 📄 生成报告
        # ------------------------------
        # 基于原始文件名生成报告，避免文件名混乱
        report_file = original_file.replace('.json', '_report.txt')
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write("=" * 70 + "\n")
            f.write("LeetCode 代码判题报告\n")
            f.write("=" * 70 + "\n\n")
            
            f.write(f"总样本数: {total}\n")
            f.write(f"通过数量: {passed}\n")
            f.write(f"失败数量: {total - passed}\n")
            f.write(f"{metric_name}: {pass_1_value:.1%}\n\n")

            # ✅ 新增难度统计
            f.write("=" * 70 + "\n")
            f.write("按难度统计（仅通过的题目）\n")
            f.write("=" * 70 + "\n")
            for diff, count in passed_by_difficulty.items():
                f.write(f"{diff:8s}: {count}\n")

            # ✅ 新增年份统计
            f.write("\n" + "=" * 70 + "\n")
            f.write("按年份统计（仅通过的题目）\n")
            f.write("=" * 70 + "\n")
            for year, count in passed_by_year.items():
                f.write(f"{year}: {count}\n")

            # ------------------------------
            # 详细结果列表
            # ------------------------------
            f.write("\n" + "=" * 70 + "\n")
            f.write("详细结果\n")
            f.write("=" * 70 + "\n\n")
            
            for i, r in enumerate(results, 1):
                status = "[OK]  " if r['passed'] else "[FAIL]"
                difficulty = difficulty_map.get(r['task_id'], 'Unknown')
                f.write(f"{i:2d}. {status} {r['task_id']:40s} ({difficulty})\n")
                if not r['passed'] and r['result']:
                    f.write(f"     -> {r['result'][:60]}\n")
            
            # ------------------------------
            # 失败题目汇总
            # ------------------------------
            f.write("\n" + "=" * 70 + "\n")
            f.write("失败的问题\n")
            f.write("=" * 70 + "\n\n")
            
            failed_problems = [r for r in results if not r['passed']]
            if failed_problems:
                for r in failed_problems:
                    difficulty = difficulty_map.get(r['task_id'], 'Unknown')
                    f.write(f"- {r['task_id']} ({difficulty}): {r['result']}\n")
            else:
                f.write("全部通过！\n")
        
        print(f"报告已生成: {report_file}")
        
        # 控制台摘要输出
        print("\n" + "=" * 70)
        print("评估摘要")
        print("=" * 70)
        print(f"\n通过题数: {passed}/{total}")
        print(f"{metric_name}: {pass_1_value:.1%}")

        print(f"\n按难度统计:")
        for diff, count in passed_by_difficulty.items():
            print(f"  {diff}: {count}")

        print(f"\n按年份统计:")
        for year, count in passed_by_year.items():
            print(f"  {year}: {count}")

        if failed_problems:
            print(f"\n失败的问题 ({len(failed_problems)} 题):")
            for r in failed_problems[:5]:
                print(f"  - {r['task_id']}")
            if len(failed_problems) > 5:
                print(f"  ... 还有 {len(failed_problems)-5} 题")
        else:
            print("\n恭喜！所有问题都通过了！")
        
        return report_file

    except Exception as e:
        print(f"生成报告失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def step5_split_results(original_file, result_file):
    """步骤5: 自动分类代码"""
    print_section("步骤 5/5: 自动分类代码")
    
    try:
        # 读取原始代码
        with open(original_file, 'r', encoding='utf-8') as f:
            original_data = json.load(f)
        
        # 读取判题结果
        results_map = {}
        with open(result_file, 'r', encoding='utf-8') as f:
            for line in f:
                result = json.loads(line)
                results_map[result['task_id']] = result['passed']
        
        # 分类
        passed_data = []
        failed_data = []
        
        for item in original_data:
            problem_slug = item['problem_slug']
            if problem_slug in results_map:
                if results_map[problem_slug]:
                    passed_data.append(item)
                else:
                    failed_data.append(item)
        
        # 保存
        passed_file = original_file.replace('.json', '_passed.json')
        failed_file = original_file.replace('.json', '_failed.json')
        
        with open(passed_file, 'w', encoding='utf-8') as f:
            json.dump(passed_data, f, ensure_ascii=False, indent=2)
        
        with open(failed_file, 'w', encoding='utf-8') as f:
            json.dump(failed_data, f, ensure_ascii=False, indent=2)
        
        print(f"[OK] 通过的代码: {passed_file} ({len(passed_data)} 题)")
        print(f"[OK] 失败的代码: {failed_file} ({len(failed_data)} 题)")
        
        if failed_data:
            print(f"\n需要修复的问题:")
            for item in failed_data[:5]:
                title = item.get('problem_title', item['problem_slug'])
                print(f"  - {title}")
            if len(failed_data) > 5:
                print(f"  ... 还有 {len(failed_data)-5} 题")
        
        return passed_file, failed_file
    
    except Exception as e:
        print(f"分类失败: {e}")
        return None, None

def main():
    """主函数"""
    print("=" * 70)
    print("LeetCode 代码判题 - 完整流程")
    print("=" * 70)
    
    # 获取输入文件
    if len(sys.argv) > 1:
        input_file = sys.argv[1]
    else:
        input_file = 'generate_code.json'
    
    print(f"\n输入文件: {input_file}")
    
    start_time = time.time()
    
    # 步骤1: 转换格式
    jsonl_file = step1_convert_format(input_file)
    if not jsonl_file:
        print("\n终止: 格式转换失败")
        return
    
    # 步骤2: 检查数据集
    if not step2_check_dataset(jsonl_file):
        print("\n终止: 数据集检查失败")
        return
    
    # 步骤3: 运行判题
    result_file, pass_at_k = step3_run_evaluation(jsonl_file)
    if not result_file:
        print("\n终止: 判题执行失败")
        return
    
    # 步骤4: 生成报告
    report_file = step4_generate_report(result_file, input_file, pass_at_k)
    
    # 步骤5: 自动分类
    passed_file, failed_file = step5_split_results(input_file, result_file)
    
    # 完成
    elapsed_time = time.time() - start_time
    
    print("\n" + "=" * 70)
    print("全部完成！")
    print("=" * 70)
    print(f"\n耗时: {elapsed_time:.1f} 秒")
    print(f"\n生成的文件:")
    print(f"  - {jsonl_file} (JSONL 格式)")
    print(f"  - {result_file} (详细结果)")
    print(f"  - {report_file} (评估报告)")
    print(f"  - {passed_file} (通过的代码)")
    print(f"  - {failed_file} (失败的代码)")
    print()

if __name__ == '__main__':
    main()
