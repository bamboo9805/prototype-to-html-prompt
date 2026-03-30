# prototype-to-html-prompt

把「原型图需求 + 接口信息 + 数据样例」压缩成可直接投喂 Cursor/Codex/Claude Code 的**高约束、低 token Prompt**，用于生成 HTML 报告页面。

> 目标：减少提示词冗长与歧义，让 AI 一次产出更接近可用代码。

---

## 适用场景

- 你有页面原型，但 AI 产出总是跑偏
- 你有 API 文档，但前端字段映射不稳定
- 你希望把团队需求转成统一 Prompt 协议（可复用、可审计）

---

## 核心能力

1. **最小输入契约**：缺失项一次性补问，避免来回拉扯。
2. **原型图压缩**：把截图压缩成固定结构（Goal/Layout/DataContract...）。
3. **低 token Prompt 生成**：短句命令式输出，减少废话和重复约束。
4. **业务 v2 生成器**：结构化 JSON -> 稳定 Prompt，输出可直接给 Cursor。

---

## 快速开始

### 方式 A：手工流程（适合临时需求）

1. 按 `SKILL.md` 收集最小输入（页面目标、模块、API、映射、交互、约束、验收）。
2. 参考 `references/prompt-templates.md` 组装 Prompt。
3. 输出时固定结构：
   - Final Prompt
   - Assumptions（如有）
   - Missing Info（如有）

### 方式 B：v2 脚本生成（推荐，适合长期业务）

```bash
cd ~/skills/prototype-to-html-prompt
python3 scripts/build_prompt_v2.py \
  --input references/business-api-profile.example.json \
  --output final-prompt.txt
```

然后把 `final-prompt.txt` 直接投喂 Cursor/Codex/Claude Code。

---

## 目录结构

```text
prototype-to-html-prompt/
├── SKILL.md                                  # 技能主说明（执行规则）
├── README.md                                 # 本文件
├── scripts/
│   └── build_prompt_v2.py                    # v2 Prompt 生成脚本
└── references/
    ├── prompt-templates.md                   # Prompt 模板
    ├── clarification-questions.md            # 补问清单
    ├── prototype-image-to-spec-compressor.md # 原型图压缩规范
    ├── business-prompt-v2.md                 # v2 说明
    ├── business-api-profile.template.json    # 业务 JSON 模板
    └── business-api-profile.example.json     # 业务 JSON 样例
```

---

## 输入/输出约定（v2）

### 输入
- 一个业务 JSON（见 `references/business-api-profile.template.json`）
- 必填核心：`goal / prototype / apis / mapping / constraints / acceptance`

### 输出
- 一段可执行 Prompt（默认命令式短句）
- 若有缺失字段，会追加：

```text
# Missing
- goal.audience
- constraints.output
...
```

---

## 质量门（建议）

在把 Prompt 发给 AI 前，至少检查：

- [ ] 页面目标是否明确（给谁看、用于什么决策）
- [ ] 模块和字段映射是否完整
- [ ] 是否定义 loading/empty/error 状态
- [ ] 技术边界是否冲突（如“原生 HTML” vs “必须 React”）
- [ ] 输出协议是否明确（仅代码 / 先方案再代码）

---

## 常见问题

### 1) 产出太长怎么办？
优先合并同类约束，删除背景叙述，保留命令句与验收标准。

### 2) 接口字段不全怎么办？
不要猜。让脚本输出 `# Missing`，一次性补齐后再生成。

### 3) 为什么建议结构化 JSON？
可复用、可 diff、可审计，且能显著降低提示词波动。

---

## License

若未单独声明，默认遵循仓库所有者后续补充的许可证策略。
