
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Generate 20-24 specification markdown files from structured source JSONs
using spec-generation-guardrail.instance.json.

Expected input directory structure:
  input/
    ipower-engine.sva.instance.json
    ipower-engine.usecase.instance.json
    ipower-engine.nfr-risk.instance.json
    ipower-engine.capability.instance.json
    ipower-engine.data-model.instance.json
    ipower-engine.document-output-model.instance.json
    ipower-engine.spec-generation-guardrail.instance.json

Usage:
  python generate_specs_from_guardrail.py --input ./input --output ./generated_specs
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any, Dict, List, Optional


SOURCE_FILE_MAP = {
    "01_overview": "ipower-engine.sva.instance.json",
    "02_sva_layers": "ipower-engine.sva.instance.json",
    "03_vertical_slices": "ipower-engine.sva.instance.json",
    "04_responsibility_boundaries": "ipower-engine.sva.instance.json",
    "05_common_data_model": "ipower-engine.sva.instance.json",
    "06_usecases": "ipower-engine.usecase.instance.json",
    "07_nfr_and_risks": "ipower-engine.nfr-risk.instance.json",
    "08_open_items": "ipower-engine.sva.instance.json",
    "09_capability_model": "ipower-engine.capability.instance.json",
    "10_data_model": "ipower-engine.data-model.instance.json",
    "11_document_output_model": "ipower-engine.document-output-model.instance.json",
}

DOC_TITLE_MAP = {
    "20_user_app_spec": "20. 家庭内アプリ仕様書（自動生成）",
    "21_cloud_backend_spec": "21. バックエンド（クラウド）仕様書（自動生成）",
    "22_hems_controller_spec": "22. HEMSコントローラ（デバイス）仕様書（自動生成）",
    "23_firmware_spec": "23. ファームウェア仕様書（自動生成）",
    "24_pcb_requirement_spec": "24. 電子基板要求仕様書（自動生成）",
}


def load_json(path: Path) -> Dict[str, Any]:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def dump_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)


def bullets(items: List[str], indent: str = "") -> str:
    if not items:
        return f"{indent}- なし"
    return "\n".join(f"{indent}- {x}" for x in items)


def yesno(value: bool) -> str:
    return "true" if value else "false"


def first_nonempty(*values: Any, default: str = "") -> str:
    for v in values:
        if v not in (None, "", [], {}):
            return str(v)
    return default


def read_sources(input_dir: Path) -> Dict[str, Dict[str, Any]]:
    data: Dict[str, Dict[str, Any]] = {}
    loaded_by_file: Dict[str, Dict[str, Any]] = {}
    for source_doc, filename in SOURCE_FILE_MAP.items():
        file_path = input_dir / filename
        if filename not in loaded_by_file:
            if not file_path.exists():
                raise FileNotFoundError(f"Missing source file: {file_path}")
            loaded_by_file[filename] = load_json(file_path)
        data[source_doc] = loaded_by_file[filename]
    return data


def parse_target_type(source_path: str) -> Optional[str]:
    m = re.search(r"target_type=([A-Za-z_]+)", source_path)
    return m.group(1) if m else None


def parse_category_filter(source_path: str) -> List[str]:
    if "category in" in source_path:
        m = re.search(r"category in \((.*?)\)", source_path)
        if m:
            return [x.strip() for x in m.group(1).split(",")]
    return []


def parse_actor_filter(source_path: str) -> List[str]:
    if "actors includes" in source_path:
        m = re.search(r"actors includes (.*)", source_path)
        if m:
            tail = m.group(1)
            return [x.strip() for x in tail.split(" or ")]
    return []


def get_overview_purpose(sources: Dict[str, Dict[str, Any]]) -> List[str]:
    return sources["01_overview"].get("product_overview", {}).get("purpose", [])


def get_vertical_slices(sources: Dict[str, Dict[str, Any]]) -> List[Dict[str, Any]]:
    return sources["03_vertical_slices"].get("vertical_slices", [])


def get_responsibility_group(sources: Dict[str, Dict[str, Any]], group_name: str) -> Dict[str, Any]:
    return sources["04_responsibility_boundaries"].get("responsibility_boundaries", {}).get(group_name, {})


def get_usecases_by_actor(sources: Dict[str, Dict[str, Any]], actors: List[str]) -> List[Dict[str, Any]]:
    result = []
    for u in sources["06_usecases"].get("usecases", []):
        uactors = set(u.get("actors", []))
        if any(a in uactors for a in actors):
            result.append(u)
    return result


def get_nfrs(
    sources: Dict[str, Dict[str, Any]],
    categories: Optional[List[str]] = None,
    related_components: Optional[List[str]] = None,
) -> List[Dict[str, Any]]:
    result = []
    for n in sources["07_nfr_and_risks"].get("non_functional_requirements", []):
        if categories and n.get("category") not in categories:
            continue
        if related_components:
            comps = set(n.get("related_component", []))
            if not any(c in comps for c in related_components):
                continue
        result.append(n)
    return result


def get_risks(sources: Dict[str, Dict[str, Any]], categories: Optional[List[str]] = None) -> List[Dict[str, Any]]:
    result = []
    for r in sources["07_nfr_and_risks"].get("risk_register", []):
        if categories and r.get("category") not in categories:
            continue
        result.append(r)
    return result


def get_open_items(sources: Dict[str, Dict[str, Any]]) -> List[Dict[str, Any]]:
    return sources["08_open_items"].get("open_items", [])


def get_capability_group(sources: Dict[str, Dict[str, Any]], target_type: str) -> Dict[str, Any]:
    for group in sources["09_capability_model"].get("capability_groups", []):
        if group.get("target_type") == target_type:
            return group
    return {"group_id": "", "target_type": target_type, "name": target_type, "capabilities": []}


def get_data_entities(sources: Dict[str, Dict[str, Any]], categories: Optional[List[str]] = None) -> List[Dict[str, Any]]:
    entities = sources["10_data_model"].get("entities", [])
    if not categories:
        return entities
    return [e for e in entities if e.get("category") in categories]


def get_doc_output(sources: Dict[str, Dict[str, Any]], document_id: str) -> Optional[Dict[str, Any]]:
    mapping = {
        "20_user_app_spec": "家庭内アプリ仕様書",
        "21_cloud_backend_spec": "クラウド仕様書",
        "22_hems_controller_spec": "HEMSコントローラ仕様書",
        "23_firmware_spec": "ファームウェア仕様書",
        "24_pcb_requirement_spec": "PCB要求仕様書",
    }
    target_name = mapping.get(document_id)
    for doc in sources["11_document_output_model"].get("output_documents", []):
        if doc.get("name") == target_name:
            return doc
    return None


def render_capability_group(group: Dict[str, Any]) -> str:
    caps = group.get("capabilities", [])
    if not caps:
        return "- なし"
    parts: List[str] = []
    for c in caps:
        parts.extend([
            f"### {c.get('name', '')}",
            f"- capability_id: {c.get('capability_id', '')}",
            f"- category: {c.get('category', '')}",
            f"- availability: {c.get('availability', '')}",
            f"- 説明: {first_nonempty(c.get('description'), default='なし')}",
            f"- 関連計測: {', '.join(c.get('related_measurement_ids', [])) or 'なし'}",
            f"- 関連コマンド: {', '.join(c.get('related_command_ids', [])) or 'なし'}",
            f"- 更新周期: {first_nonempty(c.get('update_cycle'), default='なし')}",
            f"- プロトコル: {', '.join(c.get('protocols', [])) or 'なし'}",
            "- 制約:",
            bullets(c.get("constraints", [])),
            f"- 障害時挙動: {first_nonempty(c.get('failure_behavior'), default='なし')}",
            "",
        ])
    return "\n".join(parts).rstrip()


def render_usecases(usecases: List[Dict[str, Any]]) -> str:
    if not usecases:
        return "- なし"
    parts: List[str] = []
    for u in usecases:
        parts.extend([
            f"### {u.get('title', '')}",
            f"- usecase_id: {u.get('usecase_id', '')}",
            f"- goal: {u.get('goal', '')}",
            f"- actors: {', '.join(u.get('actors', []))}",
            "- 前提条件:",
            bullets(u.get("preconditions", [])),
            "- 事後条件:",
            bullets(u.get("postconditions", [])),
            "",
        ])
    return "\n".join(parts).rstrip()


def render_entities(entities: List[Dict[str, Any]]) -> str:
    if not entities:
        return "- なし"
    parts: List[str] = []
    for e in entities:
        parts.extend([
            f"### {e.get('name', '')}",
            f"- entity_id: {e.get('entity_id', '')}",
            f"- category: {e.get('category', '')}",
            f"- 説明: {first_nonempty(e.get('description'), default='なし')}",
            "- 主なフィールド:",
        ])
        for f in e.get("fields", []):
            parts.append(
                f"  - {f.get('field_name','')} "
                f"({f.get('data_type','')}, required={yesno(bool(f.get('required', False)))}, "
                f"source={first_nonempty(f.get('source_type'), default='なし')})"
            )
        parts.append("")
    return "\n".join(parts).rstrip()


def render_nfrs(nfrs: List[Dict[str, Any]]) -> str:
    if not nfrs:
        return "- なし"
    parts: List[str] = []
    for n in nfrs:
        parts.extend([
            f"### {n.get('title', '')}",
            f"- nfr_id: {n.get('nfr_id', '')}",
            f"- category: {n.get('category', '')}",
            f"- requirement: {n.get('requirement', '')}",
            f"- target_value: {first_nonempty(n.get('target_value'), default='TBD')}",
            f"- verification_method: {n.get('verification_method', '')}",
            "",
        ])
    return "\n".join(parts).rstrip()


def render_risks(risks: List[Dict[str, Any]]) -> str:
    if not risks:
        return "- なし"
    parts: List[str] = []
    for r in risks:
        parts.extend([
            f"### {r.get('title', '')}",
            f"- risk_id: {r.get('risk_id', '')}",
            f"- category: {r.get('category', '')}",
            f"- probability: {r.get('probability', '')}",
            f"- impact: {r.get('impact', '')}",
            f"- priority: {r.get('priority', '')}",
            f"- mitigation: {r.get('mitigation', '')}",
            f"- poc_validation: {r.get('poc_validation', '')}",
            "",
        ])
    return "\n".join(parts).rstrip()


def render_open_items(open_items: List[Dict[str, Any]]) -> str:
    if not open_items:
        return "- なし"
    parts: List[str] = []
    for o in open_items:
        parts.extend([
            f"### {o.get('title', '')}",
            f"- item_id: {o.get('item_id', '')}",
            f"- status: {o.get('status', '')}",
            f"- owner: {first_nonempty(o.get('owner'), default='TBD')}",
            f"- 内容: {first_nonempty(o.get('description'), default='TBD')}",
            "",
        ])
    return "\n".join(parts).rstrip()


def render_traceability_table(spec_rule: Dict[str, Any]) -> str:
    parts = [
        "## Appendix A. Source Traceability",
        "",
        "| Section | Source Document | Source Path | Usage Rule | Required |",
        "|---|---|---|---|---|",
    ]
    for sec in spec_rule.get("required_sections", []):
        for src in sec.get("source_requirements", []):
            parts.append(
                f"| {sec.get('title','')} | {src.get('source_document','')} | "
                f"{src.get('source_path','')} | {src.get('usage_rule','')} | "
                f"{yesno(bool(src.get('required', False)))} |"
            )
    return "\n".join(parts)


def summary_from_overview(sources: Dict[str, Dict[str, Any]]) -> str:
    overview = sources["01_overview"].get("product_overview", {})
    purpose = overview.get("purpose", [])
    vision = overview.get("vision", "")
    lines = []
    if vision:
        lines.append(vision)
    if purpose:
        lines.append("主目的:")
        lines.extend([f"- {x}" for x in purpose])
    return "\n".join(lines) if lines else "TBD"


def generate_spec_document(spec_rule: Dict[str, Any], sources: Dict[str, Dict[str, Any]], tbd_marker: str) -> str:
    doc_id = spec_rule["document_id"]
    title = DOC_TITLE_MAP.get(doc_id, doc_id)
    overview_summary = summary_from_overview(sources)
    open_items = get_open_items(sources)

    target_type_map = {
        "20_user_app_spec": "user_app",
        "21_cloud_backend_spec": "cloud",
        "22_hems_controller_spec": "hems_controller",
        "23_firmware_spec": "hems_controller",
        "24_pcb_requirement_spec": "hems_controller",
    }

    actor_map = {
        "20_user_app_spec": ["user", "user_app"],
        "21_cloud_backend_spec": ["cloud"],
        "22_hems_controller_spec": ["edge_controller"],
        "23_firmware_spec": ["edge_controller"],
        "24_pcb_requirement_spec": ["edge_controller"],
    }

    entity_category_map = {
        "20_user_app_spec": ["measurement", "derived_metric", "alert", "policy"],
        "21_cloud_backend_spec": ["measurement", "event", "command", "policy", "alert", "device_state", "sync_status", "audit_log", "derived_metric"],
        "22_hems_controller_spec": ["measurement", "event", "command", "device_state", "sync_status"],
        "23_firmware_spec": ["measurement", "event", "command", "device_state", "sync_status"],
        "24_pcb_requirement_spec": [],
    }

    nfr_component_map = {
        "20_user_app_spec": ["user_app"],
        "21_cloud_backend_spec": ["cloud"],
        "22_hems_controller_spec": ["edge_controller", "network"],
        "23_firmware_spec": ["edge_controller", "network"],
        "24_pcb_requirement_spec": ["edge_controller", "network"],
    }

    risk_category_map = {
        "20_user_app_spec": ["ux_app", "data_integrity_quality"],
        "21_cloud_backend_spec": ["data_integrity_quality", "security"],
        "22_hems_controller_spec": ["communication_data_acquisition", "ota_firmware", "security"],
        "23_firmware_spec": ["communication_data_acquisition", "ota_firmware", "security"],
        "24_pcb_requirement_spec": ["communication_data_acquisition", "ota_firmware", "security"],
    }

    capability_group = get_capability_group(sources, target_type_map.get(doc_id, ""))
    usecases = get_usecases_by_actor(sources, actor_map.get(doc_id, []))
    entities = get_data_entities(sources, entity_category_map.get(doc_id, []))
    nfrs = get_nfrs(sources, related_components=nfr_component_map.get(doc_id, []))
    risks = get_risks(sources, risk_category_map.get(doc_id, []))
    responsibility_map = {
        "20_user_app_spec": None,
        "21_cloud_backend_spec": "cloud",
        "22_hems_controller_spec": "edge_controller",
        "23_firmware_spec": "edge_controller",
        "24_pcb_requirement_spec": None,
    }
    responsibility = None
    if responsibility_map.get(doc_id):
        responsibility = get_responsibility_group(sources, responsibility_map[doc_id])

    parts = [
        f"# {title}",
        "",
        "## 1. 文書情報",
        f"- document_id: {doc_id}",
        f"- output_file: {spec_rule.get('output_file', '')}",
        f"- audience: {spec_rule.get('audience', '')}",
        f"- style: {spec_rule.get('generation_rules', {}).get('style', '')}",
        "",
        "## 2. 概要",
        overview_summary or tbd_marker,
        "",
    ]

    if responsibility:
        parts.extend([
            "## 3. 責務",
            "- responsibilities:",
            bullets(responsibility.get("responsibilities", [])),
            "- must_not_do:",
            bullets(responsibility.get("must_not_do", [])),
            "- failure_mode_behavior:",
            bullets(responsibility.get("failure_mode_behavior", [])),
            "",
        ])

    parts.extend([
        "## 4. Capability / 機能要求",
        render_capability_group(capability_group),
        "",
        "## 5. 関連ユースケース",
        render_usecases(usecases),
        "",
    ])

    if entities:
        parts.extend([
            "## 6. 扱うデータ",
            render_entities(entities),
            "",
        ])

    parts.extend([
        "## 7. 必須トピック（Guardrail由来）",
        bullets(spec_rule.get("required_topics", [])),
        "",
        "## 8. 禁止トピック（Guardrail由来）",
        bullets(spec_rule.get("forbidden_topics", [])),
        "",
        "## 9. 非機能要件",
        render_nfrs(nfrs),
        "",
        "## 10. リスク・留意事項",
        render_risks(risks),
        "",
    ])

    if spec_rule.get("generation_rules", {}).get("must_include_open_items", False):
        parts.extend([
            "## 11. 未決事項 / Open Items",
            render_open_items(open_items),
            "",
        ])

    parts.extend([
        render_traceability_table(spec_rule),
        "",
    ])

    return "\n".join(parts).rstrip() + "\n"


def generate_guardrail_report(guardrail: Dict[str, Any]) -> str:
    parts = [
        "# Guardrail Execution Report",
        "",
        "## Global Policy",
        f"- TBD marker: {guardrail['global_rules']['tbd_policy'].get('tbd_marker','TBD')}",
        f"- do_not_guess_missing_values: {yesno(guardrail['global_rules']['tbd_policy'].get('do_not_guess_missing_values', True))}",
        f"- require_source_traceability: {yesno(guardrail['global_rules']['traceability_policy'].get('require_source_traceability', True))}",
        "",
        "## Documents",
    ]
    for doc in guardrail.get("spec_documents", []):
        parts.extend([
            f"### {doc['document_id']}",
            f"- output_file: {doc['output_file']}",
            f"- style: {doc.get('generation_rules', {}).get('style', '')}",
            f"- max_assumption_level: {doc.get('generation_rules', {}).get('max_assumption_level', '')}",
            f"- allowed_sources: {', '.join(doc.get('allowed_sources', []))}",
            "",
        ])
    return "\n".join(parts)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, help="Input directory containing source JSON files")
    parser.add_argument("--output", required=True, help="Output directory for generated markdown files")
    args = parser.parse_args()

    input_dir = Path(args.input)
    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)

    guardrail_path = input_dir / "ipower-engine.spec-generation-guardrail.instance.json"
    if not guardrail_path.exists():
        raise FileNotFoundError(f"Missing guardrail instance: {guardrail_path}")

    guardrail = load_json(guardrail_path)
    sources = read_sources(input_dir)
    tbd_marker = guardrail["global_rules"]["tbd_policy"].get("tbd_marker", "TBD")

    for spec_rule in guardrail.get("spec_documents", []):
        content = generate_spec_document(spec_rule, sources, tbd_marker)
        dump_text(output_dir / spec_rule["output_file"], content)

    dump_text(output_dir / "guardrail_execution_report.md", generate_guardrail_report(guardrail))
    print(f"Generated files in: {output_dir}")


if __name__ == "__main__":
    main()
