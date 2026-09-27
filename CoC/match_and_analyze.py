import json

def match_and_analyze():
    """
    从cognitive_complexity_results.json中提取与generate_code_passed.json匹配的数据并进行分析
    """
    
    # 读取generate_code_passed.json
    print("正在读取 generate_code_passed.json...")
    with open('generate_code_passed.json', 'r', encoding='utf-8') as f:
        generated_codes = json.load(f)
    
    # 读取cognitive_complexity_results.json
    print("正在读取 cognitive_complexity_results.json...")
    with open('cognitive_complexity_results.json', 'r', encoding='utf-8') as f:
        complexity_data = json.load(f)
    
    # 匹配数据
    print("\n正在匹配数据...")
    matched_data = []
    not_found = []
    
    for item in generated_codes:
        problem_id = item['problem_id']
        problem_slug = item['problem_slug']
        
        # 构建文件名
        filename = f"{problem_id}-{problem_slug}.py"
        
        # 在complexity_data中查找匹配项
        if filename in complexity_data:
            matched_item = {
                'problem_id': problem_id,
                'problem_slug': problem_slug,
                'difficulty': item['difficulty'],
                'language': item['language'],
                'estimated_date': item['estimated_date'],
                'cognitive_complexity': int(complexity_data[filename]),
                'filename': filename,
                'generated_code': item['generated_code']
            }
            matched_data.append(matched_item)
        else:
            not_found.append({
                'problem_id': problem_id,
                'problem_slug': problem_slug,
                'filename': filename
            })
    
    # 保存匹配的数据
    print(f"\n成功匹配 {len(matched_data)} 条数据")
    with open('matched_complexity_data.json', 'w', encoding='utf-8') as f:
        json.dump(matched_data, f, ensure_ascii=False, indent=2)
    print("已保存匹配数据到 matched_complexity_data.json")
    
    # 如果有未匹配的数据，保存到单独的文件
    if not_found:
        print(f"\n有 {len(not_found)} 条数据未找到匹配项")
        with open('not_found_items.json', 'w', encoding='utf-8') as f:
            json.dump(not_found, f, ensure_ascii=False, indent=2)
        print("未匹配项已保存到 not_found_items.json")
    
    # 进行数据分析
    print("\n" + "="*80)
    print("数据分析结果")
    print("="*80)
    
    # 基础统计
    print(f"\n【基础统计】")
    print(f"总数据条数: {len(generated_codes)}")
    print(f"成功匹配: {len(matched_data)}")
    print(f"未匹配: {len(not_found)}")
    print(f"匹配率: {len(matched_data)/len(generated_codes)*100:.2f}%")
    
    if matched_data:
        # 认知复杂度统计
        complexities = [item['cognitive_complexity'] for item in matched_data]
        avg_complexity = sum(complexities) / len(complexities)
        max_complexity = max(complexities)
        min_complexity = min(complexities)
        
        print(f"\n【认知复杂度统计】")
        print(f"平均复杂度: {avg_complexity:.2f}")
        print(f"最高复杂度: {max_complexity}")
        print(f"最低复杂度: {min_complexity}")
        
        # 找出最高和最低复杂度的题目
        max_items = [item for item in matched_data if item['cognitive_complexity'] == max_complexity]
        min_items = [item for item in matched_data if item['cognitive_complexity'] == min_complexity]
        
        print(f"\n最高复杂度的题目 ({len(max_items)}个):")
        for item in max_items[:5]:  # 只显示前5个
            print(f"  - {item['filename']}: {item['cognitive_complexity']}")
        
        print(f"\n最低复杂度的题目 ({len(min_items)}个):")
        for item in min_items[:5]:  # 只显示前5个
            print(f"  - {item['filename']}: {item['cognitive_complexity']}")
        
        # 按难度统计
        print(f"\n【按难度统计】")
        difficulty_stats = {}
        for item in matched_data:
            diff = item['difficulty']
            if diff not in difficulty_stats:
                difficulty_stats[diff] = {
                    'count': 0,
                    'total_complexity': 0,
                    'complexities': []
                }
            difficulty_stats[diff]['count'] += 1
            difficulty_stats[diff]['total_complexity'] += item['cognitive_complexity']
            difficulty_stats[diff]['complexities'].append(item['cognitive_complexity'])
        
        for diff in ['Easy', 'Medium', 'Hard']:
            if diff in difficulty_stats:
                stats = difficulty_stats[diff]
                avg = stats['total_complexity'] / stats['count']
                print(f"{diff}: {stats['count']}题, 平均复杂度: {avg:.2f}")
        
        # 复杂度分布
        print(f"\n【复杂度分布】")
        complexity_ranges = {
            '0-5': 0,
            '6-10': 0,
            '11-15': 0,
            '16-20': 0,
            '21+': 0
        }
        
        for complexity in complexities:
            if complexity <= 5:
                complexity_ranges['0-5'] += 1
            elif complexity <= 10:
                complexity_ranges['6-10'] += 1
            elif complexity <= 15:
                complexity_ranges['11-15'] += 1
            elif complexity <= 20:
                complexity_ranges['16-20'] += 1
            else:
                complexity_ranges['21+'] += 1
        
        for range_name, count in complexity_ranges.items():
            percentage = count / len(complexities) * 100
            bar = '█' * int(percentage / 2)
            print(f"{range_name:>8}: {count:>3} ({percentage:>5.1f}%) {bar}")
        
        # 按日期统计（年月）
        print(f"\n【按时间统计（前10个月）】")
        date_stats = {}
        for item in matched_data:
            date = item['estimated_date'][:7]  # 只取年-月
            if date not in date_stats:
                date_stats[date] = {
                    'count': 0,
                    'total_complexity': 0
                }
            date_stats[date]['count'] += 1
            date_stats[date]['total_complexity'] += item['cognitive_complexity']
        
        sorted_dates = sorted(date_stats.items())
        for date, stats in sorted_dates[:10]:  # 只显示前10个
            avg = stats['total_complexity'] / stats['count']
            print(f"{date}: {stats['count']:>3}题, 平均复杂度: {avg:.2f}")
        
        # 生成简化的CSV文件用于进一步分析
        print(f"\n正在生成CSV文件...")
        with open('complexity_analysis.csv', 'w', encoding='utf-8') as f:
            f.write("problem_id,problem_slug,difficulty,cognitive_complexity,estimated_date\n")
            for item in matched_data:
                f.write(f"{item['problem_id']},{item['problem_slug']},{item['difficulty']},{item['cognitive_complexity']},{item['estimated_date']}\n")
        print("已保存CSV文件到 complexity_analysis.csv")
    
    print("\n" + "="*80)
    print("分析完成！")
    print("="*80)
    
    return matched_data, not_found

if __name__ == "__main__":
    matched_data, not_found = match_and_analyze()

