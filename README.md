# 实验基础指标测量工具 / Public Metric Utilities

本目录提供基础指标的通用测量工具，供读者检查测量口径、运行小型示例，或对自行提供的代码进行测量。

这是**部分源码公开版本**，仅覆盖下文列出的独立测量功能，不构成完整论文复现包。示例均为专门编写的演示数据，不代表论文实验结果。

## 指标与口径

| 指标 | 实现与方向 | 范围及限制 |
| --- | --- | --- |
| 功能正确性 / pass@k | 保留 LeetCodeDataset 执行器；通过率越大越好 | 执行调用者提供的完整 `test`，而非仅比较一个示例；不额外声称对所有可能输入正确 |
| ET | `time.perf_counter()`，毫秒，越小越好 | `tracemalloc` 开启时的一次目标调用；排除进程启动、模块导入、对象构造及 JSON 输入复制 |
| MU | `tracemalloc.get_traced_memory()` 的峰值，字节，越小越好 | 不等于进程 RSS，不代表全部原生库或 GPU 分配；目标调用前已分配的输入不计入 |
| MI | Radon 6.0.1 `mi_visit(source, multi=True)`，越大越好 | 对完整原始源文件计算；同时保留 Radon 等级；无法分析的文件单独记录，未计入均值 |
| CoC | Sonar 原始 `CognitiveComplexityVisitor.complexity(fileInput, None)`，越小越好 | 整文件口径，保留插件哈希和 Java 版本；不使用手写近似规则 |
| 排序一致性 | SciPy Spearman ρ / Kendall τ-b | 输入两个按同一候选顺序排列的名次数组；小名次代表靠前；支持并列，常量向量结果为 `null` |

ET/MU 默认重复 5 次，每次在新 Python 子进程执行相同输入，报告原始测量、均值与样本标准差。任一次超时或异常，该次运行整体标为失败，不将部分成功值平均为完整结果。性能入口**不验证正确性**；需要正确代码子集时，应先独立判题并明确记录过滤规则。

正确率报告区分样本通过率与按题等权的 pass@k。对每题的 n 个样本、c 个正确样本，使用 `1 - C(n-c,k)/C(n,k)`；只有每题均满足 `n >= k` 时才报告该 k，否则列入 `unavailable_k`。这两种统计在每题样本数不等时可能不同，不应混用。

## 安装与示例

推荐 Python 3.10+，Linux / WSL。以下命令均从本 README 所在目录执行：

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt

python -m metrics.correctness --problems examples/problems.jsonl --samples examples/samples.jsonl --k 1 --output outputs/correctness.json
python -m metrics.performance examples/performance_case.json --repeats 5 --output outputs/performance.json
python -m metrics.maintainability examples/solution.py --output outputs/mi.json
python -m metrics.agreement examples/ranks.json --output outputs/agreement.json
python -m unittest discover -s tests -v
```

正确性和性能入口会执行提供的 Python 代码。子进程及执行器内置的保护不是安全沙箱，应在隔离环境中运行不可信代码。示例执行器不自动下载数据、不调用模型服务。

CoC 需要调用者另外准备 SonarQube、Java 和可用的 Python 分析器。此入口的兼容目标为 SonarQube Server 2025.1 LTA；版本不同可能导致结果变化。该接口调用分析器内部类，其他版本不保证兼容。

```bash
python -m pip install -r requirements-coc.txt
python -m metrics.cognitive examples/solution.py --sonarqube /path/to/sonarqube --jvm /path/to/libjvm.so --output outputs/coc.json
```

脚本要求 `lib/` 下恰有一个 `sonar-python-plugin-*.jar`；分析器二进制不随包提供。完整 CoC 运行需要在准备好上述环境后另行验证。

## 换成自己的输入

- **正确性**：`problems.jsonl` 每行含唯一 `task_id`、`prompt`、`test`、`entry_point`；执行程序按 `prompt + completion + test + check(entry_point)` 拼接。`samples.jsonl` 每行含 `task_id` 和完整 `completion`。同题可有多个独立生成样本；两份输入的题目集合必须一致，不自动丢掉未尝试的题目。
- **性能**：JSON 包含 `source`（相对配置文件目录）、`entry_point`（模块级函数或无参构造的 `Class.method`）、JSON 可表示的 `args` 和 `kwargs`。每个配置代表一个固定输入。链表、树、特殊依赖需由调用者提供适配模块。模块导入产生的顶层调用仍可能执行，但不计入 ET/MU。
- **MI / CoC**：可传单个源文件或专用源码目录；目录会递归扫描所有 `.py`，应避免将虚拟环境、工具自身或其他代码混入待测目录。
- **相关系数**：JSON 含 `ranks_a` 与 `ranks_b`，两数组长度相同、位置一一对应。

MI 和 CoC 将解析失败单独记录并以非零状态退出；性能失败也以非零状态退出。判题不通过属于正常评估结果，请读取报告中的 `passed` 和通过率。输出可能包含调用者输入的任务名或运行时错误文本；不要未经检查就将真实运行输出提交到公开仓库。

## 可复现范围与文件

`metrics/` 是通用入口，`third_party/` 保留判题执行器及许可证，`examples/` 为演示示例，`tests/` 检查指标边界和执行失败处理，`RELEASE_MANIFEST.json` 记录分发文件的 SHA-256。

本包仅附带演示示例。测量结果受到输入、候选代码、解释器、依赖及硬件影响；示例输出不能用于宣称复现论文数值。其他数据和代码需由读者自行提供，并遵守各自许可。第三方来源和许可边界见 [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md)。
