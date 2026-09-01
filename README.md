# Competition Repository Template v0.1.0

这是一个**真实比赛项目仓库模板**。它不负责告诉队伍“第几小时必须做什么”，也不内置固定的 Q1→Q2→Q3→Q4 流程。

它只解决四件事：

1. 让题面事实、假设、数据、模型、代码、Run、结果和论文有明确落点；
2. 让三人协作时不互相覆盖、不丢失关键结果；
3. 让论文中的关键结论可以追溯到真实 Run 和 Git commit；
4. 给 Coach 与 SkillHub 一个**自然的人类可读工作区**，而不是额外的 API/YAML 接口。

## 核心原则：仓库记录事实，不规定比赛流程

顶层防僵化原则见 `DESIGN_GUARDRAILS.md`。后续扩展模板时也应服从它。

- `PROJECT_STATUS.md` 是当前项目状态快照，不是阶段门禁。
- `problem/` 保存事实、问题结构、假设与歧义。
- `models/` 保存模型合同；`src/` 保存实现；二者分离。
- `runs/` 保存会影响结论的计算记录；失败 Run 也可以保留。
- `results/` / `figures/` 保存可被论文引用的结果。
- `audit/` 保存为什么这样做、论文主张由什么支撑。
- `paper/` 提供 Word/Markdown 与 LaTeX 两条生产线，但**实际比赛只维护一条 active track**。

## 开赛时怎么用

1. 复制本模板并初始化 Git。
2. 将原题和附件放入 `problem/statement/`、`data/raw/`，原始文件保持只读。
3. 填 `problem/FACTS.md` 和 `problem/QUESTION_MAP.md`。
4. 根据实际题目动态增加问题目录：

```bash
python scripts/add_question.py q1
python scripts/add_question.py q2 --paper-track latex
```

这只是创建文件夹，不意味着必须按 q1、q2 的顺序求解。

5. 需要保存一次有意义的运行时：

```bash
python scripts/new_run.py --question q2 --model baseline
```

6. 随时更新 `PROJECT_STATUS.md`。它应反映**当前最大风险和下一项值得做的决定**，而不是“现在进入了哪个阶段”。

## 与 Coach / SkillHub 搭配

### Coach

把本仓库根目录作为比赛工作区。Coach 优先读取：

- `PROJECT_STATUS.md`
- `problem/QUESTION_MAP.md`
- `problem/FACTS.md`
- `audit/DECISION_LOG.md`
- `runs/RUN_LEDGER.csv`
- `audit/CLAIM_EVIDENCE_MAP.csv`

Coach 的职责是根据当前状态判断“现在最值得处理什么”，而不是机械推进目录或阶段。

### SkillHub

把本仓库根目录作为 `PROJECT_ROOT`。SkillHub 直接读取已有事实并把产物写回对应目录，例如：

- 模型选择/合同 → `models/<question>/`
- 代码/调试 → `src/<question>/`
- 实验 → `runs/`、`results/`
- 图表 → `figures/`
- 论文审计 → `audit/`

不要求先生成额外的接口文件。

## 目录

```text
.
├── PROJECT_STATUS.md
├── DESIGN_GUARDRAILS.md
├── TEAM.md
├── COLLABORATION.md
├── problem/
├── data/
├── models/
├── src/
├── runs/
├── results/
├── figures/
├── references/
├── paper/
├── audit/
├── ai/
└── scripts/
```

## 非目标

本模板不会强制：

- 固定小时数；
- 固定问题数量；
- 固定模型数量；
- 固定图数/页数；
- 固定角色分支；
- 每个小步骤都审批；
- 没有 Reviewer/Subagent 就阻塞整个比赛。

当届官方规则始终高于本模板。
