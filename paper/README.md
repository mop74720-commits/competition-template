# Paper Production

本模板提供两条论文生产线：

- `latex/`：分章节 LaTeX 工程；
- `word/`：Markdown/Word 生产线的内容入口。

**不要求开赛时立刻选，也不建议同时维护两份正文。** 当论文生产真正开始后，选择一个 active track；另一条仅作为备用/转换目标。

论文只引用已经能追溯到 `runs/`、`results/`、`figures/` 或已核验文献的证据。

## LaTeX 构建

`paper/latex/` 由 `build.py` 作为唯一构建逻辑来源；Makefile 与 PowerShell 只是薄封装，避免 Linux / Windows 两套脚本长期漂移。

常用命令：

```bash
cd paper/latex
make draft
make review
make release
make print
make all
make clean
```

Windows：

```powershell
cd paper/latex
./make.ps1 draft
./make.ps1 review
./make.ps1 release
./make.ps1 print
```

也可直接运行：

```bash
python build.py release --profile generic
```

构建产物写入 `paper/latex/build/`，不同目标分别生成 `draft.pdf`、`review.pdf`、`release.pdf` 和 `print.pdf`。

### 构建语义

- `draft`：日常编辑版本；
- `review`：打开 overfull box 标记，用于排版检查；
- `release`：面向电子提交，隐藏超链接样式；
- `print`：面向打印，隐藏超链接样式；
- `all`：依次构建上述四种版本；
- `clean`：清理 `build/` 中的生成物。

构建使用 `-halt-on-error` 和超时控制。目标 PDF 只在完整编译成功后产生；旧的同名目标会在新构建开始前清理，避免把历史 PDF 误认为本次成功结果。

如 `main.tex` 实际使用 BibTeX 或 Biber，构建器会在第一次 XeLaTeX 后自动识别并运行相应后端，再完成必要的重复编译。

## Format Profiles

`paper/latex/profiles/` 用于接入不同比赛/届次的论文模板。默认 `generic` profile 继续使用仓库自带的通用 `main.tex`。

**不要把某个历史年份的第三方 CUMCM `.cls` 直接固化成永久默认模板。** 当届 CUMCM 官方模板应作为新的 profile/entrypoint 接入，并由当届 `rules/` 事实层与 `validate_submission.py` 共同核验。

示例配置见：

- `latex/profiles/generic.json`
- `latex/profiles/cumcm-current.example.json`
- `latex/profiles/README.md`

格式 profile 只解决“怎样生成该格式的论文”；不会改变模型、Run、证据或比赛决策。

当届官方模板与规则优先于本目录中的任何默认格式。
