# HEMS SVA Markdown Generator

## 含まれるもの
- templates/*.md.j2  … Markdownテンプレート
- generate_md.py     … 生成スクリプト

## 入力ファイル (案件フォルダに配置)
案件フォルダ内に以下の3つの instance json を配置する:
- *.sva.instance.json       … SVA定義 (概要・レイヤー・責務境界・データモデル等)
- *.usecase.instance.json   … ユースケース定義
- *.nfr-risk.instance.json  … 非機能要件・リスク定義

例: instances/0138_i-power/
  ipower-engine.sva.instance.json
  ipower-engine.usecase.instance.json
  ipower-engine.nfr-risk.instance.json

## 実行方法
python generate_md.py <案件フォルダのパス>

例:
  python generate_md.py ../instances/0138_i-power/

## 生成物
指定した案件フォルダ内に generated_md/ が作成される:
<案件フォルダ>/generated_md/
- 00_full_document.md
- 01_overview.md
- 02_sva_layers.md
- 03_vertical_slices.md
- 04_responsibility_boundaries.md
- 05_common_data_model.md
- 06_usecases.md
- 07_nfr_and_risks.md
- 08_open_items.md

## 使い方の基本
1. 案件フォルダに instance json 3本を配置
2. python generate_md.py <案件フォルダ> を実行
3. 生成された md をレビュー
4. 最後に docx 化して客先提出

## 次の拡張候補
- Wordテンプレートへの自動差し込み
- Mermaid/SVG図の自動生成
- JSON validation の追加
