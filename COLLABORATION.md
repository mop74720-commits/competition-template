# Collaboration Guide

## Git 原则

- `main` 保持**可恢复、可理解**，不要求每一刻都达到最终提交质量。
- 使用短生命周期分支：`work/q2-baseline`、`work/figure-demand`、`fix/unit-mismatch`。
- 不建议永久设置 `modeling` / `coding` / `paper` 三条角色分支；角色会随比赛变化，长期分叉更容易造成冲突。
- 能小步合并就不要积累半天后一次性大合并。
- 不要在 Git 中提交密码、API Key、个人隐私或竞赛规则禁止公开的材料。

## 提交信息

推荐让提交说明包含对象和关键变化，例如：

```text
feat(q2): add capacity-constrained baseline
fix(q3): correct angle unit deg -> rad
result(q2): objective 153.82 -> 148.67; R014
paper(q1): sync final value with R009
```

若提交改变了论文关键数字，优先在 message 或 `audit/DECISION_LOG.md` 中写清变化。

## 三人协作

目录不是“角色领地”。任何人都可以修改任何目录，但同一时刻尽量只有一个人编辑同一个权威文件。

最容易冲突的文件：

- `PROJECT_STATUS.md`
- `problem/FACTS.md`
- `audit/DECISION_LOG.md`
- 论文主文件

对于这些文件，先沟通再编辑；其他代码/实验尽量按问题或任务拆分。

## 合并前最小检查

- 新结果是否真的来自当前代码？
- 单位/参数口径是否变化？
- 若关键结论变化，是否更新 Run Ledger / Decision Log / Claim-Evidence？
- 是否误把大体积临时文件提交进 Git？
