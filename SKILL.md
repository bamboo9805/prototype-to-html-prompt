---
name: prototype-to-html-prompt
description: 将“原型图需求 + 接口信息 + 数据样例”压缩成可直接投喂 Cursor/Codex/Claude Code 的高约束、低 token Prompt，用于生成 HTML 报告页面。当用户想做报表类页面、但提示词冗长或不够明确时使用。
---

# Prototype to HTML Prompt（中文注释版）

将输入整理成**短、准、可执行**的工程 Prompt，默认面向 Cursor 生成 HTML 报告页。

## 工作流（按顺序执行）

1. 收集最小输入；缺失则一次性补问。  
2. 将原型信息压缩为结构化规范（Layout/DataContract/Constraints）。  
3. 选择模板生成 Prompt（或走 v2 生成器）。  
4. 对 Prompt 做压缩与歧义检查。  
5. 输出最终 Prompt + 假设项 + 缺失项。

## 1）最小输入契约（缺一补问）

仅保留必需字段，避免开放式长问答。

- 页面目标：这张报告给谁看、用来做什么决策。
- 原型结构：模块清单（图表/表格/指标卡/筛选区/时间范围）。
- 接口清单：`method + url + params + response schema + 鉴权`。
- 字段映射：UI 组件字段 ← API 字段。
- 交互规则：筛选、排序、分页、刷新、空态、报错。
- 技术边界：原生 HTML 或 React、是否允许第三方库。
- 输出要求：单文件/多文件、是否只返回代码。
- 验收标准：成功条件（可运行、字段完整、响应式、错误处理）。

如果缺失，最多提 6 个问题，使用编号：`Q1..Q6`。

## 2）原型图压缩

当输入包含原型截图时：

1. 先读 `references/prototype-image-to-spec-compressor.md`。  
2. 将原型图压缩成固定 7 段结构（Goal/Layout/DataContract/Interactions/VisualRules/Constraints/Acceptance）。  
3. 信息不足只放到 `Missing Info`，不要编造接口字段。

## 3）Prompt 生成规则（低 token）

生成 Prompt 时执行：

1. 只写命令句，不写背景解释。
2. 去掉重复约束与礼貌性废话。
3. 同类约束合并成一段。
4. 用键值短句替代长段落。
5. 明确输出协议（仅代码 / 先方案后代码）。
6. 不确定项写成 `Assumption:` 单行。

目标：

- 单页报告 Prompt：建议 <= 220 中文 token（约）
- 多模块报告 Prompt：建议 <= 350 中文 token（约）

## 4）业务专属 Prompt 生成器 v2

当用户已有稳定业务接口时，优先使用结构化输入 + 脚本生成：

1. 参考 `references/business-api-profile.example.json` 建立业务 JSON。  
2. 使用 `scripts/build_prompt_v2.py` 生成最终 Prompt。  
3. 若脚本输出 `# Missing`，先补齐再投喂 Cursor。  

脚本用途：降低人工措辞波动，稳定 Prompt 长度和准确度。

## 5）输出格式（对用户可见）

始终按以下结构输出：

### A. Final Prompt（给 Cursor）

输出一个代码块，直接可复制。

### B. Assumptions（如有）

仅列必要假设，每条 <= 1 行。

### C. Missing Info（如有）

用 `Q1..Qn` 列出补充问题，问题必须可直接回答。

## 6）质量闸门（生成前自检）

发布 Prompt 前检查：

- 是否包含页面目标、模块、接口、字段映射、验收。
- 是否有模糊词：`合适地/尽量/美观一些`（有则替换为可验收标准）。
- 是否指定输出格式（只代码 or 先方案后代码）。
- 是否限制技术栈与文件边界。
- 是否存在冲突要求（如“纯原生”与“必须 React 组件”并存）。

## References

- 模板：`references/prompt-templates.md`
- 补问清单：`references/clarification-questions.md`
- 原型图压缩器：`references/prototype-image-to-spec-compressor.md`
- 业务 v2 生成器说明：`references/business-prompt-v2.md`
- 业务 JSON 模板：`references/business-api-profile.template.json`
- 业务 JSON 样例：`references/business-api-profile.example.json`

## Scripts

- Prompt v2 构建：`scripts/build_prompt_v2.py`
