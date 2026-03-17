# HEMS SVA Starter Pack

このパックは、HEMS/SVA設計フローを一式で回すための最小スターターです。

## フォルダ構成

- `input/schemas/`
  - schema 一式
- `input/instances/`
  - i-Power Engine の instance JSON 一式
- `scripts/`
  - `generate_md.py`
  - `generate_specs_from_guardrail.py`
  - `md_to_docx.py`
  - `run_all.py`
- `example_output/`
  - 生成済みの 20〜24 仕様書サンプル

## 基本フロー

### 1. 上位設計を更新
更新対象:
- `ipower-engine.sva.instance.json`
- `ipower-engine.usecase.instance.json`
- `ipower-engine.nfr-risk.instance.json`
- `ipower-engine.capability.instance.json`
- `ipower-engine.data-model.instance.json`
- `ipower-engine.document-output-model.instance.json`
- `ipower-engine.spec-generation-guardrail.instance.json`

### 2. 20〜24 の仕様書を自動生成
```bash
python scripts/generate_specs_from_guardrail.py --input input/instances --output generated/spec_md
```

### 3. 必要に応じて md を統合
例えば:
- `20_user_app_spec.md`
- `21_cloud_backend_spec.md`
- `22_hems_controller_spec.md`
- `23_firmware_spec.md`
- `24_pcb_requirement_spec.md`

を 1 本の `full_specs.md` に結合してから Word 化する。

### 4. docx 化
`md_to_docx.py` は Markdown → DOCX 用の雛形です。
必要に応じて、入力 md を差し替えて使ってください。

## Guardrail の役割

- 参照可能な source JSON を制限
- 必須セクションを強制
- 禁止トピックを明示
- TBD / Open Items を保持
- 責務境界を越えた自動補完を防止
- Source traceability を残す

## 推奨の次ステップ

- `generate_md.py` を 09〜12 まで含めて拡張
- `run_all.py` を 01〜24 の完全生成に拡張
- `md_to_docx.py` を複数文書一括変換対応に拡張
- traceability appendix を docx 側にも出力
