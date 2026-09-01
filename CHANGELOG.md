# Changelog

## 0.2.0

- 新增当前届次 `rules/` 事实层和 submission-only validator。
- 官方规则未核验不阻塞科学工作，但硬阻止 submission-ready。
- 新增支撑材料构建/manifest 与 AI 详情模板。
- AI 合规以真实日志为证据，禁止补造。
- submission validator 执行 `blocking_unknowns`，并在 rule profile 明确要求时检查 A4、首页摘要、支撑 ZIP 源程序与 AI 详情。

### Integration-audit fixes

全系统演练与集成审计修复：

- 新增 `contest_import.py`，复制/哈希原始题面和附件并生成 advisory preflight；
- DOCX 同时读取 python-docx 可见结构与 OOXML 全文本，降低文本框/对象漏读风险；
- PDF 支持文本量检查与可选页面渲染，不默认 OCR；
- 自动提取数字、范围、上下限和单位候选，但不自动升级为 FACT；
- 新增 `SOURCE_MANIFEST.csv` / `PREFLIGHT_REPORT.md`；
- 新增可选 `results/final/submission/` staging 位置；
- AI usage log 改为只记录重大 AI 介入，避免形成流程负担。
