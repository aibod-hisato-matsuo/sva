import json
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parent
TEMPLATE_DIR = BASE / "templates"


def find_instance_file(folder: Path, suffix: str) -> Path:
    """Find a single *.<suffix>.instance.json file in folder."""
    matches = list(folder.glob(f"*.{suffix}.instance.json"))
    if len(matches) == 0:
        print(f"Error: no *.{suffix}.instance.json found in {folder}", file=sys.stderr)
        sys.exit(1)
    if len(matches) > 1:
        print(f"Error: multiple *.{suffix}.instance.json found in {folder}: {matches}", file=sys.stderr)
        sys.exit(1)
    return matches[0]

def load_json(path: Path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def load_template(name: str) -> str:
    return (TEMPLATE_DIR / name).read_text(encoding="utf-8")

def bullets(items):
    if not items:
        return "- なし"
    return "\n".join(f"- {x}" for x in items)

def bool_ja(v):
    return "はい" if v else "いいえ"

def render_user_modes(modes):
    if not modes:
        return "- 定義なし"
    chunks = []
    for m in modes:
        chunks.append("\n".join([
            f"### {m.get('name','')}",
            f"- ID: {m.get('mode_id','')}",
            f"- 説明: {m.get('description','')}",
            f"- ユーザー承認必須: {bool_ja(m.get('requires_user_approval', False))}",
            f"- 自動化レベル: {m.get('automation_level','')}",
        ]))
    return "\n\n".join(chunks)

def render_layers(layers):
    order = ["L0", "L1", "L2", "L3", "L4", "L5"]
    chunks = []
    for key in order:
        layer = layers.get(key, {})
        chunks.append("\n".join([
            f"## {key}: {layer.get('title','')}",
            f"- 意図: {layer.get('intent','')}",
            f"- 主要要素:",
            bullets(layer.get("key_elements", [])),
            f"- 制約:",
            bullets(layer.get("constraints", [])),
        ]))
    return "\n\n".join(chunks)

def render_vertical_slices(slices):
    if not slices:
        return "- 定義なし"
    chunks = []
    for s in slices:
        chunks.append("\n".join([
            f"## {s.get('name','')}",
            f"- ID: {s.get('slice_id','')}",
            f"- ゴール: {s.get('goal','')}",
            f"- トリガー: {s.get('trigger','')}",
            f"- 必要データ:",
            bullets(s.get("required_data", [])),
            f"- 判断ロジック:",
            bullets(s.get("decision_logic", [])),
            f"- 実行対象:",
            bullets(s.get("execution_targets", [])),
            f"- UI接点:",
            bullets(s.get("ui_touchpoints", [])),
            f"- フォールバック: {s.get('fallback_behavior','')}",
            f"- 関連ユースケース:",
            bullets(s.get("related_usecase_ids", [])),
        ]))
    return "\n\n".join(chunks)

def render_responsibility(boundaries):
    labels = {
        "edge_controller": "HEMSコントローラ",
        "cloud": "クラウド",
        "user_app": "家庭内アプリ",
        "admin_app": "管理者アプリ",
    }
    chunks = []
    for key in ["edge_controller", "cloud", "user_app", "admin_app"]:
        g = boundaries.get(key, {})
        chunks.append("\n".join([
            f"## {labels[key]}",
            f"- 主責務:",
            bullets(g.get("responsibilities", [])),
            f"- やってはいけないこと:",
            bullets(g.get("must_not_do", [])),
            f"- 障害時挙動:",
            bullets(g.get("failure_mode_behavior", [])),
        ]))
    return "\n\n".join(chunks)

def render_channels(channels):
    if not channels:
        return "- 定義なし"
    return "\n\n".join("\n".join([
        f"### {c.get('name','')}",
        f"- ID: {c.get('channel_id','')}",
        f"- 方向: {c.get('direction','')}",
        f"- 説明: {c.get('description','')}",
    ]) for c in channels)

def render_measurements(measurements):
    if not measurements:
        return "- 定義なし"
    return "\n\n".join("\n".join([
        f"### {m.get('name','')}",
        f"- ID: {m.get('measurement_id','')}",
        f"- 区分: {m.get('category','')}",
        f"- 単位: {m.get('unit','')}",
        f"- 取得チャネル: {', '.join(m.get('source_channels', []))}",
        f"- 推定許可: {bool_ja(m.get('is_estimation_allowed', False))}",
        f"- 推定フラグ必須: {bool_ja(m.get('estimation_flag_required', False))}",
        f"- 備考: {m.get('notes','')}",
    ]) for m in measurements)

def render_events(events):
    if not events:
        return "- 定義なし"
    return "\n\n".join("\n".join([
        f"### {e.get('name','')}",
        f"- ID: {e.get('event_id','')}",
        f"- 重大度: {e.get('severity','')}",
        f"- 説明: {e.get('description','')}",
    ]) for e in events)

def render_usecases(usecases):
    if not usecases:
        return "- 定義なし"
    chunks = []
    for u in usecases:
        main_flow = "\n".join(
            f"{step.get('step_no')}. [{step.get('actor')}] {step.get('action')}"
            for step in u.get("main_flow", [])
        ) or "- なし"
        alt_flow_chunks = []
        for alt in u.get("alternative_flows", []):
            alt_flow_chunks.append("\n".join([
                f"#### 条件: {alt.get('condition','')}",
                bullets(alt.get("flow", []))
            ]))
        alt_text = "\n\n".join(alt_flow_chunks) if alt_flow_chunks else "- なし"
        chunks.append("\n".join([
            f"## {u.get('title','')}",
            f"- ID: {u.get('usecase_id','')}",
            f"- ゴール: {u.get('goal','')}",
            f"- アクター: {', '.join(u.get('actors', []))}",
            f"- 前提条件:",
            bullets(u.get("preconditions", [])),
            f"- メインフロー:",
            main_flow,
            f"- 代替フロー:",
            alt_text,
            f"- 事後条件:",
            bullets(u.get("postconditions", [])),
            f"- 関連レイヤー: {', '.join(u.get('related_layers', []))}",
            f"- 関連リスク: {', '.join(u.get('related_risk_ids', [])) or 'なし'}",
        ]))
    return "\n\n".join(chunks)

def render_nfr(nfrs):
    if not nfrs:
        return "- 定義なし"
    return "\n\n".join("\n".join([
        f"### {n.get('title','')}",
        f"- ID: {n.get('nfr_id','')}",
        f"- 区分: {n.get('category','')}",
        f"- 要求: {n.get('requirement','')}",
        f"- 目標値: {n.get('target_value','')}",
        f"- 検証方法: {n.get('verification_method','')}",
        f"- 関連コンポーネント: {', '.join(n.get('related_component', []))}",
    ]) for n in nfrs)

def render_risks(risks):
    if not risks:
        return "- 定義なし"
    return "\n\n".join("\n".join([
        f"### {r.get('title','')}",
        f"- ID: {r.get('risk_id','')}",
        f"- 区分: {r.get('category','')}",
        f"- 発生確率: {r.get('probability','')}",
        f"- 影響度: {r.get('impact','')}",
        f"- 優先度: {r.get('priority','')}",
        f"- 内容: {r.get('description','')}",
        f"- 緩和策: {r.get('mitigation','')}",
        f"- PoC検証: {r.get('poc_validation','')}",
        f"- 状態: {r.get('status','')}",
    ]) for r in risks)

def render_open_items(open_items):
    if not open_items:
        return "- 定義なし"
    return "\n\n".join("\n".join([
        f"## {o.get('title','')}",
        f"- ID: {o.get('item_id','')}",
        f"- 状態: {o.get('status','')}",
        f"- オーナー: {o.get('owner','')}",
        f"- 内容: {o.get('description','')}",
    ]) for o in open_items)

def main():
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <input_folder>", file=sys.stderr)
        print(f"  e.g. python {sys.argv[0]} ../instances/0138_i-power/", file=sys.stderr)
        sys.exit(1)

    input_folder = Path(sys.argv[1]).resolve()
    if not input_folder.is_dir():
        print(f"Error: {input_folder} is not a directory", file=sys.stderr)
        sys.exit(1)

    OUTPUT_DIR = input_folder / "generated_md"
    OUTPUT_DIR.mkdir(exist_ok=True)

    sva = load_json(find_instance_file(input_folder, "sva"))
    usecase = load_json(find_instance_file(input_folder, "usecase"))
    nfr_risk = load_json(find_instance_file(input_folder, "nfr-risk"))

    overview = load_template("01_overview.md.j2").format(
        project_name=sva["document_info"]["project_name"],
        version=sva["document_info"]["version"],
        status=sva["document_info"]["status"],
        language=sva["document_info"]["language"],
        last_updated=sva["document_info"].get("last_updated", ""),
        vision=sva["product_overview"]["vision"],
        purpose_bullets=bullets(sva["product_overview"]["purpose"]),
        scope_bullets=bullets(sva["product_overview"]["scope"]),
        out_of_scope_bullets=bullets(sva["product_overview"]["out_of_scope"]),
        user_modes_section=render_user_modes(sva["product_overview"].get("user_modes", [])),
    )
    layers = load_template("02_sva_layers.md.j2").format(layers_section=render_layers(sva["sva_layers"]))
    vertical = load_template("03_vertical_slices.md.j2").format(vertical_slices_section=render_vertical_slices(sva.get("vertical_slices", [])))
    responsibilities = load_template("04_responsibility_boundaries.md.j2").format(
        responsibility_section=render_responsibility(sva["responsibility_boundaries"])
    )
    data_model = load_template("05_common_data_model.md.j2").format(
        channels_section=render_channels(sva["common_data_model"].get("channels", [])),
        measurements_section=render_measurements(sva["common_data_model"].get("measurements", [])),
        events_section=render_events(sva["common_data_model"].get("events", [])),
        flag_required=bool_ja(sva["common_data_model"]["estimated_value_rule"]["flag_required"]),
        ui_distinction_required=bool_ja(sva["common_data_model"]["estimated_value_rule"]["ui_distinction_required"]),
        estimated_notes=sva["common_data_model"]["estimated_value_rule"].get("notes", ""),
    )
    usecases = load_template("06_usecases.md.j2").format(usecases_section=render_usecases(usecase.get("usecases", [])))
    nfr_and_risks = load_template("07_nfr_and_risks.md.j2").format(
        nfr_section=render_nfr(nfr_risk.get("non_functional_requirements", [])),
        risk_section=render_risks(nfr_risk.get("risk_register", [])),
    )
    open_items = load_template("08_open_items.md.j2").format(open_items_section=render_open_items(sva.get("open_items", [])))

    outputs = {
        "01_overview.md": overview,
        "02_sva_layers.md": layers,
        "03_vertical_slices.md": vertical,
        "04_responsibility_boundaries.md": responsibilities,
        "05_common_data_model.md": data_model,
        "06_usecases.md": usecases,
        "07_nfr_and_risks.md": nfr_and_risks,
        "08_open_items.md": open_items,
    }
    for filename, content in outputs.items():
        (OUTPUT_DIR / filename).write_text(content, encoding="utf-8")

    merged = "\n\n".join([overview, layers, vertical, responsibilities, data_model, usecases, nfr_and_risks, open_items])
    (OUTPUT_DIR / "00_full_document.md").write_text(merged, encoding="utf-8")

if __name__ == "__main__":
    main()
