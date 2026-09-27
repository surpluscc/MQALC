import json
from datetime import datetime
from statistics import mean
from collections import defaultdict


def generate_report_txt(
    meta_path: str = "matched_complexity_data.json",
    output_path: str = "cognitive_complexity_report.txt",
):
    """
    直接基于 matched_complexity_data.json 进行分析:
      - 该文件本身就包含 cognitive_complexity、difficulty 等信息
      - 不再单独读取 cognitive_complexity_results.json
    """
    with open(meta_path, "r", encoding="utf-8") as f:
        items = json.load(f)

    # 构建带元数据的列表
    entries = []
    for item in items:
        filename = item.get("filename")
        if not filename:
            continue
        try:
            complexity = float(item.get("cognitive_complexity"))
        except (TypeError, ValueError):
            # 跳过没有/无法解析复杂度的记录
            continue

        problem_id = item.get("problem_id", "未知")
        slug = item.get("problem_slug") or filename.rsplit(".", 1)[0]
        difficulty = item.get("difficulty", "Unknown")
        language = item.get("language", "python3")

        entries.append(
            {
                "filename": filename,
                "complexity": complexity,
                "problem_id": problem_id,
                "slug": slug,
                "difficulty": difficulty,
                "language": language,
            }
        )

    total_files = len(entries)
    if total_files == 0:
        print("没有可用的 Cognitive Complexity 数据。")
        return

    # 全局统计
    complexities = [e["complexity"] for e in entries]
    avg_complexity = mean(complexities)
    max_entry = max(entries, key=lambda e: e["complexity"])
    min_entry = min(entries, key=lambda e: e["complexity"])

    # 按难度分类统计
    by_difficulty = defaultdict(list)
    for e in entries:
        by_difficulty[e["difficulty"]].append(e)

    # 生成报告文本
    lines = []
    lines.append("=" * 80)
    lines.append("JSON 代码 Cognitive Complexity 分析报告")
    lines.append("=" * 80)
    lines.append("")
    lines.append(f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append(f"数据来源: {meta_path}")
    lines.append(f"代码总数: {total_files}")
    lines.append(f"成功分析: {total_files} 个")
    lines.append(f"数据来源文件中记录总数: {len(items)} 条")
    lines.append("")
    lines.append("-" * 80)
    lines.append("统计摘要")
    lines.append("-" * 80)
    lines.append("")
    lines.append(f"平均 Cognitive Complexity: {avg_complexity:.2f}")
    lines.append(
        f"最高复杂度: {max_entry['complexity']:.0f} "
        f"(问题ID: {max_entry['problem_id']}, 难度: {max_entry['difficulty']}, 文件: {max_entry['filename']})"
    )
    lines.append(
        f"最低复杂度: {min_entry['complexity']:.0f} "
        f"(问题ID: {min_entry['problem_id']}, 难度: {min_entry['difficulty']}, 文件: {min_entry['filename']})"
    )
    lines.append("")
    # 按难度分类统计
    lines.append("-" * 80)
    lines.append("按题目难度(LeetCode)分类统计")
    lines.append("-" * 80)
    lines.append("")

    for difficulty in ["Easy", "Medium", "Hard", "Unknown"]:
        group = by_difficulty.get(difficulty, [])
        if not group:
            continue
        group_complexities = [e["complexity"] for e in group]
        group_avg = mean(group_complexities)
        count = len(group)

        lines.append(f"{difficulty}:")
        lines.append(f"  数量: {count} 个")
        lines.append(f"  平均 Cognitive Complexity: {group_avg:.2f}")
        lines.append("")

    # 详细列表（可根据需要缩减）
    lines.append("-" * 80)
    lines.append("每个代码的详细 Cognitive Complexity")
    lines.append("-" * 80)
    lines.append("")

    # 为了可读性，按 problem_id + filename 排序
    def sort_key(e):
        try:
            return int(e["problem_id"]), e["filename"]
        except (TypeError, ValueError):
            return (10**9, e["filename"])

    for idx, e in enumerate(sorted(entries, key=sort_key), start=1):
        lines.append(
            f"{idx}. 问题ID: {e['problem_id']} | {e['slug']} "
            f"({e['filename']})"
        )
        lines.append(
            f"   难度: {e['difficulty']} | 语言: {e['language']}"
        )
        lines.append(
            f"   Cognitive Complexity: {e['complexity']:.0f}"
        )
        lines.append("")

    # 将报告写入文件
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"报告已生成: {output_path}")


if __name__ == "__main__":
    generate_report_txt()

