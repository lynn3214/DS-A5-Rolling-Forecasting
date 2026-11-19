# Dataset selection record

本文件保留 Phase 1C 的历史可行性审计。当前研究决定已由 Evaluation Protocol v1.0 更新并冻结：使用 MetroPT-3 / TP2 / 600 秒 horizon；原始 Phase 1C 提案仅作历史记录。

## Phase 1C feasibility recommendation (historical)

## 历史建议：选择 MetroPT-3（Phase 1C）

**PASS（候选可行性）**：本地 MetroPT-3 原始 CSV 已完整读取，1,516,948 行、近七个月跨度、无重复时间戳、无解析失败，10 秒采样间隔为众数，足以规划五个非平凡 chronological rolling origins。观察到长断档，因此评估必须明确连续窗口和断档排除规则。此 PASS 只针对数据用于 retrospective rolling evaluation 的可行性，不代表时间戳实时可用或模型有效。

UR3 CobotOps **FAIL（主要候选）**：7,409 行的表只覆盖约 7 小时；863 个 timestamp 无效且存在约 5.23 小时最大缺口。缺少足够独立时期支持五个可信 origins、季节基线与漂移评估。

| 维度 | MetroPT-3 | UR3 |
|---|---|---|
| 研究相关性 | 真实列车压缩机压力/温度/电流 | 真实协作机器人运行测量 |
| 实际可访问性 | 本地完整 CSV 可读取 | 本地 XLSX 可读取，CRC 通过 |
| 时间可靠性 | 单调、无重复、无时区，10s 众数但强烈不规则 | UTC 时间字符串但 863 无效值，短跨度且巨型缺口 |
| 特征 | 压力、温度、电流及离散状态 | 六轴电流/温度/速度、工具电流、保护停机等 |
| 五 origins | 可规划，需连续段约束 | 不建议作为可靠长期 rolling evaluation |
| 漂移/关键期 | 多月运行可探索，故障报告时间需谨慎对齐 | 多时期证据不足 |
| 计算成本 | CSV 208 MB，合理 | XLSX 1.7 MB，低 |
| 可复现性 | 原始文件有哈希；CC BY 4.0 | 原始文件有哈希；CC BY 4.0 |
| DS-A5 失败风险 | 中：时钟/间隔/availability 和缺口处理 | 高：时间覆盖及无效 timestamp |

## Phase 2 前置实验定义（不在此执行）

- Target：TP2 pressure；issue time：已完成、可用采样时刻 `t`；horizon：下一个约 10 秒采样点。
- Sampling：10 秒主频（经验众数）；要先定因果性对齐策略并限制连续时段。
- Features：已观测 TP2、TP3、H1、Motor_current、Oil_temperature、已完成状态信号。
- Baselines：persistence 必需；24-hour seasonal naive 仅在映射点存在、无跨缺口时纳入。
- Evaluation：至少五个按时间前进的 expanding origins，按可用连续窗口选取；训练边界和预测窗口不得跨长断档。
- Critical periods：可预定义故障报告窗口，但报告与传感器时钟对齐是未知项；状态段可作辅助切片。不能用 test target 定义实时告警期。
- 风险：不清楚时区/采集时钟误差和历史发布延迟；缺口与采样节奏变化；按故障时间打标签的误差；全数据预处理、前向填充、lookahead rolling features 和测试期筛选泄漏。

Phase 1C 结束时的建议文字保留作历史记录；之后用户批准并冻结了 Phase 2A Evaluation Protocol v1.0。Phase 2B 尚未开始。

## Phase 2A horizon update

Historical Phase 1C proposed a 10-second TP2 horizon. Phase 2A superseded that proposal with a 600-second horizon based only on development-period diagnostics: the 10-second pair correlation is approximately 0.946, while the corrected future-only 600-second pair correlation is approximately 0.255, with 98.29% eligible coverage after the 60-second gap rule. The one-hour horizon has low match coverage. This is a task-design choice, not evidence of forecasting skill. See `results/audit/forecasting_task_diagnostics.json`; Evaluation Protocol v1.0 has since been approved and frozen; model skill and live availability remain unverified.

## Phase 2A supersedes the original horizon proposal

The Phase 1C section above preserves its historical 10-second proposal. Phase 2A superseded it with 600 seconds using development-only diagnostics. The frozen protocol specifies future-only matching, 60-second gap eligibility, and exact feature/baseline rules. Dataset selection remains MetroPT-3; this does not assert model skill or live availability. See `docs/evaluation_protocol_v1.md`.
