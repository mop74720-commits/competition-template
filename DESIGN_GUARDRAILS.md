# Design Guardrails

本文件定义模板的顶层不变量，防止后续版本越做越像僵硬流水线。

## 1. State over Stage

仓库可以描述当前状态，但不应存在一个强制全局字段把项目锁成：

`READ -> MODEL -> CODE -> WRITE -> SUBMIT`

真实比赛允许不同问题同时处于不同成熟度，也允许回退、并行和跳转。

## 2. Evidence over Ceremony

只有在能提高正确性、复现性或最终一致性时才增加记录。不要为了“流程完整”制造审批、报告和 manifest。

## 3. Dynamic question count

不预设 q1–q4。题目有几问就动态创建几问；问题标签也可用 `partA`、`task2b` 等。

## 4. Short-lived branches over role branches

不把三名队员永久锁进 modeling/coding/paper 分支。按当前任务开短分支，尽快合并。

## 5. Advisory checks by default

普通 QA 默认返回风险与证据；只有以下情况天然具有硬约束属性：

- 明确违反题面/官方规则；
- 数学/数值结果已被证伪；
- 最终产物无法打开/编译/复现；
- 关键主张与证据冲突。

其他“最佳实践”不得伪装成官方硬门槛。

## 6. One source of truth per fact

题面事实、当前 Final Run、正式图表、论文主张都应有清晰权威来源；但不要求所有临时探索都做重型版本治理。

## 7. Coach decides priorities; SkillHub solves local problems

- Coach 可以读取仓库状态并改变当前优先级；
- SkillHub 可以返回局部风险和建议，但不能自行决定放弃某问、冻结全局模型或提交。

## 8. The template serves humans first

如果某个自动化设计让队员必须维护大量 YAML/状态码才能继续比赛，应优先删掉或降级它。

## 9. Preflight is evidence assistance, not a new stage

赛题导入、hash、文本抽取、页面渲染和数字/范围候选扫描用于降低漏读硬约束的风险。它们不能自动宣布“读题完成”，也不能把未人工核对的候选直接升级为 FACT。


## 10. Official rules may block submission, not exploration

当前届次官方规则是一级事实。规则未核验时，队伍仍可继续读题、建模、实现和验证，但不得宣称 `SUBMISSION_READY`。规则 profile 只是官方全文的机器伴随索引，不得反过来成为繁琐流程。

## 11. AI disclosure is evidence

AI 使用记录不得为了合规而事后补造。若官方要求模型版本、关键交互或人工核验，而历史证据缺失，应明确记录为 blocker。


## 12. Selection is exploratory; Competition Repo is formal

Selection Workspace 允许临时假设、失败 probe 和候选路线，但不是正式事实源。不得自动把 selection 猜测写入 `problem/FACTS.md`。

## 13. Information gain over exhaustive scoring

多题选择优先验证最可能改变选择的决定性未知。固定 0–5 权重、固定分差、固定 Day-One gate 只能作为启发，不能成为模板门槛。
