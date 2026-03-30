#!/usr/bin/env python3
"""
根据“原型 + 接口”的结构化 JSON，生成简洁、可执行的 Prompt（面向 Cursor/Codex/Claude Code）。

用法示例：
  python scripts/build_prompt_v2.py --input references/business-api-profile.example.json
  python scripts/build_prompt_v2.py --input my-profile.json --output final-prompt.txt
"""

import argparse
import json
from pathlib import Path
from typing import Any, Dict, List, Tuple


# 生成 Prompt 所需的顶层关键字段。
REQUIRED_KEYS = ["goal", "prototype", "apis", "mapping", "constraints", "acceptance"]


def _get(d: Dict[str, Any], path: str, default=None):
    """按点路径安全取值。

    例如 path="goal.audience"，当中间节点不存在时返回 default。
    """
    cur = d
    for p in path.split("."):
        if not isinstance(cur, dict) or p not in cur:
            return default
        cur = cur[p]
    return cur


def validate(profile: Dict[str, Any]) -> List[str]:
    """校验 profile 最小必填项，返回缺失字段路径列表。"""
    missing: List[str] = []

    # 1) 先校验顶层结构。
    for k in REQUIRED_KEYS:
        if k not in profile:
            missing.append(k)

    # 2) 再校验关键子字段（决定 Prompt 可执行性）。
    if not _get(profile, "goal.audience"):
        missing.append("goal.audience")
    if not _get(profile, "goal.decision"):
        missing.append("goal.decision")
    if not _get(profile, "prototype.modules"):
        missing.append("prototype.modules")
    if not _get(profile, "constraints.stack"):
        missing.append("constraints.stack")
    if not _get(profile, "constraints.output"):
        missing.append("constraints.output")

    return missing


def compact_api(api: Dict[str, Any]) -> str:
    """将单个 API 压缩为一行短描述，降低 token 消耗。"""
    method = api.get("method", "GET")
    url = api.get("url", "")
    params = api.get("params", {})
    keys = api.get("responseKeys", [])
    auth = api.get("auth", "")

    # params/responseKeys 仅保留“字段名摘要”，不展开详细 schema。
    p = ",".join(params.keys()) if isinstance(params, dict) else str(params)
    r = ",".join(keys) if isinstance(keys, list) else str(keys)

    line = f"{method} {url}; p:{p or '-'}; r:{r or '-'}"
    if auth:
        line += f"; auth:{auth}"
    return line


def compact_mapping(mapping: List[Dict[str, str]], max_items: int = 12) -> str:
    """压缩 UI 字段映射。

    只截取前 max_items 项，避免映射过长导致 Prompt 膨胀。
    """
    pairs: List[str] = []
    for item in mapping[:max_items]:
        ui = item.get("ui", "")
        api = item.get("api", "")
        if ui and api:
            pairs.append(f"{ui}<-{api}")
    return "; ".join(pairs)


def build_prompt(profile: Dict[str, Any]) -> Tuple[str, List[str]]:
    """构造最终 Prompt，并返回缺失项列表。"""
    missing = validate(profile)

    # 目标信息
    audience = _get(profile, "goal.audience", "")
    decision = _get(profile, "goal.decision", "")
    business_topic = _get(profile, "goal.topic", "业务报告")

    # 页面结构信息
    modules = _get(profile, "prototype.modules", [])
    layout = _get(profile, "prototype.layout", "从上到下")
    module_text = "; ".join(
        [m.get("name", "未命名模块") for m in modules if isinstance(m, dict)]
    )

    # 接口信息压缩
    apis = _get(profile, "apis", [])
    api_lines = [compact_api(a) for a in apis if isinstance(a, dict)]

    # 字段映射压缩
    mapping = _get(profile, "mapping", [])
    mapping_text = compact_mapping(mapping)

    # 交互规则
    interactions = _get(profile, "interactions", [])
    interactions_text = "/".join(interactions) if interactions else "筛选/排序/分页/刷新"

    # 技术约束
    stack = _get(profile, "constraints.stack", "原生HTML+CSS+JS")
    output = _get(profile, "constraints.output", "single-file")
    libs = _get(profile, "constraints.allowLibs", [])
    libs_text = ",".join(libs) if libs else "无"
    code_only = _get(profile, "constraints.codeOnly", True)

    # 验收标准
    acceptance = _get(profile, "acceptance", [])
    acceptance_text = "; ".join(acceptance) if acceptance else "可运行/字段正确/状态完整"

    # 输出协议：代码直出 or 先方案后代码
    output_protocol = "仅输出代码，不要解释" if code_only else "先给计划，再给完整代码"

    # 组装最终 Prompt（保持短句、可执行、低冗余）
    prompt = (
        "你是资深前端工程师。按约束生成报告页。\n"
        f"目标: 为{audience}提供{business_topic}报告，用于{decision}。\n"
        f"模块: {module_text or '-'}；布局:{layout}。\n"
        "接口:\n"
        + "\n".join([f"{i+1}) {line}" for i, line in enumerate(api_lines)])
        + "\n"
        f"映射: {mapping_text or '-'}。\n"
        f"交互: {interactions_text}；状态: loading/empty/error 必须实现。\n"
        f"技术: {stack}；输出文件:{output}；三方库:{libs_text}。\n"
        f"验收: {acceptance_text}。\n"
        f"输出协议: {output_protocol}"
    )

    return prompt.strip(), missing


def main() -> None:
    """命令行入口：读取 JSON -> 生成 Prompt -> 输出到 stdout 或文件。"""
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, help="业务 profile JSON 路径")
    parser.add_argument("--output", help="可选：输出文件路径")
    args = parser.parse_args()

    # 读取输入并生成 Prompt。
    data = json.loads(Path(args.input).read_text(encoding="utf-8"))
    prompt, missing = build_prompt(data)

    # 将缺失项附加到输出末尾，便于一次性补齐。
    missing_block = ""
    if missing:
        missing_block = "\n\n# Missing\n" + "\n".join([f"- {m}" for m in missing])

    text = prompt + missing_block + "\n"

    # 支持落盘或直接打印。
    if args.output:
        Path(args.output).write_text(text, encoding="utf-8")
    else:
        print(text)


if __name__ == "__main__":
    main()
