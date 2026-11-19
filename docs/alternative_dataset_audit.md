# Phase 1C 本地数据集可行性审计

## 结论摘要

MetroPT-3 **通过作为 DS-A5 候选**，适合做有明确缺口处理规则的历史传感器连续值滚动预测；UR3 CobotOps 不适合作为主要时间序列候选：原表仅覆盖约 7 小时，时间戳字段有 863/7409 条无法解析，且没有证据支持将其视为多时段连续运行数据。推荐 MetroPT-3，但 Phase 2 开始前仍需审阅本报告并确定采样重整规则。

## 文件、格式与来源

本地原始文件：`data/raw/metropt3/MetroPT3(AirCompressor).csv`、同目录 PDF；`data/raw/ur3/dataset_02052023.xlsx`。脚本只读源文件，不排序、插补或写回。CSV 有 1,516,948 数据行，大小 218,300,507 bytes，SHA-256 `db30ccb4ea402e3c8bf2c99db06e288d4f2a772f6928f9dbe26a920d69793e24`。XLSX ZIP 完整性检查通过，大小 1,771,022 bytes，SHA-256 `f0f10917de9056908a82cec1aa459ddf9da2d2db70d269b128f99241c8796091`。完整机器输出见 `results/audit/alternative_audit.json`。

官方来源及许可见 `sources.md`：UCI MetroPT-3 (DOI 10.24432/C5VW3R) 与 UR3 CobotOps (DOI 10.24432/C5J891)，页面均标 CC BY 4.0。此前网络下载失败记录保留于同一 JSON 的 `prior_download_failures`；本次只用用户提供的本地文件。

## MetroPT-3 实测

- **VERIFIED**：列 `index, timestamp` 与 15 个测量/状态字段；所有 timestamp 均可解析，无时区信息，范围 2020-02-01 00:00:00 至 2020-09-01 03:59:50。时间戳非递减且重复数为 0。
- **VERIFIED**：众数间隔 10 秒，占 1,337,521 个相邻差值；另有 9、11、12、13 秒等间隔，最大相邻差 172,918 秒（约 47.98 小时）。这实证支持约 0.1 Hz，而非 1 Hz；实际记录节奏并非严格等间隔。
- **VERIFIED**：CSV 实测字段缺失值统计为零（包括离散数字字段），但此结论不代表所有数值有效或采集连续。长间隔显示大量断档；因此不能把全局重采样/前向填充当成观测事实。
- **VERIFIED**：传感器包括 TP2、TP3、H1、DV_pressure、Reservoirs、Oil_temperature、Motor_current 与阀/状态信号。电流和状态字段能区分设备状态；用于描述状态变化可行。未建立任何预测性能结论。
- **VERIFIED**：近七个月时间覆盖、约 10 秒常见频率和充足行数，允许提出至少五个按时间排序的滚动切分候选；但需以连续观测段/固定时间网格建立窗口，并排除跨越长断档的窗口。模型未训练，origins 仅属设计可行性判断。
- **UNKNOWN**：无时区字段，不清楚设备时钟基准/漂移；传感器值的真实采集时刻与落盘/可用时刻没有独立发布日志。传感器行时间戳可作为事件时间候选，不可当作实时可用时间证明。

官方描述的 1Hz 与 0.1Hz 不一致，由实测 10 秒众数间隔支持 0.1Hz。故障报告时间仅作为外部记录，不假设与采样点精准对齐。

## UR3 CobotOps 实测

XLSX 只有 `data` 工作表，7409 行、24 列（比 UCI 页面“20 features”展示项多，按文件列为准）；XLSX 容器 CRC 检查通过。`Timestamp` 表示为可解析 UTC 字符串 6546 行，863 行无效；有效时间范围 2022-10-26 08:17:21.847Z 至 15:36:06.580Z。有效时间戳升序且无重复，众数间隔约 1.005 秒，但最大缺口 18,814.125 秒；这一巨大缺口与缺失时间戳意味着数据不是可直接视作均匀连续序列的 7409 样本。Cycle 字段不是经过验证的 elapsed time，不用其代替真实时间。尽管有效片段可能足够做短时切分，整体跨度和时间戳有效性不足以支撑可靠的五个长期 rolling origins、季节基线或跨时期漂移判断。

## 任务可行性与 point-in-time

建议 MetroPT-3 目标为 `TP2` 压力，或根据业务优先级改选 `Motor_current`；本建议只把 TP2 作为唯一 primary target。假设预测时刻 `t` 是一条采样记录完成采集且可用的时刻，预测 `t+10s` 的 TP2；真实采样不规则时必须先制定因果性规则。历史特征仅使用 `t` 及之前已完成的 TP2、TP3、H1、Motor_current、Oil_temperature 和状态信号。可比较 persistence 与 24 小时季节朴素基线；后者只有在对应历史时点存在、且间隔/缺口策略明确时才成立。主模型选择留待 Phase 2，不在本阶段训练。

五个 expanding origins 可按时间段从早期至后期预先定点，但必须依据真实连续有效窗口和固定 horizon 筛选；切分时不能跨越 172,918 秒级断档。Critical period 可预注册为故障报告所列空气泄漏时间窗，作为外部事件描述，并报告时间对齐不确定性；也可用只基于训练历史的运行状态规则。用测试期目标值筛选高压/高电流段只能称 post-hoc 描述，不能作为部署触发器。

主要泄漏风险：用全量数据估计缩放参数；向前/向后填充跨断档；滚动统计含当前未完成采样；目标派生状态过滤；依据故障报告时间直接贴标签；全量筛选“正常”记录；test误差驱动特征/站点选择；把样本索引、cycle 序号误当时间。所有预处理必须按训练窗口重拟合。

## 执行记录

执行：`conda run -n nussem1 python scripts/audit_alternatives.py`，退出码 0；完整统计及文件指纹写入 `results/audit/alternative_audit.json`。MetroPT 全量 CSV 读取、UR3 全部 sheet 读取及 ZIP CRC 检查均完成。审计代码修正了旧版只统计 CSV 行数/少量 timestamp 示例、把 XLSX 当作仅列 ZIP 成员、以及无数据类型/缺失/时序分析的问题。执行了 `python -m py_compile scripts/audit_alternatives.py`，通过。未生成模型或合成数据。
