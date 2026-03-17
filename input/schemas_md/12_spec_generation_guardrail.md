# 12. Specification Generation Guardrail

## 概要
- 01〜11 の上位文書から 20〜24 の派生仕様書を生成する際のガイドライン／ガードレールを定義する。
- 目的は、未定義仕様の発明を防ぎ、責務境界とトレーサビリティを保持すること。

## Global Rules

### Allowed Source Documents
- 01_overview
- 02_sva_layers
- 03_vertical_slices
- 04_responsibility_boundaries
- 05_common_data_model
- 06_usecases
- 07_nfr_and_risks
- 08_open_items
- 09_capability_model
- 10_data_model
- 11_document_output_model

### Inference Policy
- section structure inference: true
- wording normalization: true
- minor editorial completion: true
- forbid undefined function invention: true
- forbid undefined hw detail invention: true
- forbid undefined api detail invention: true
- notes: 章立て補完・文体統一・軽微な編集補完は許可。未定義の機能、HW詳細、API詳細の発明は禁止。

### TBD Policy
- use_tbd_marker_for_missing_information: true
- collect_open_items_from_sources: true
- do_not_guess_missing_values: true
- tbd_marker: TBD

### Traceability Policy
- require_source_traceability: true
- require_section_to_source_mapping: true
- mapping_style: appendix_table

## 20_user_app_spec
- output_file: 20_user_app_spec.md
- audience: customer_facing
- allowed_sources:
  - 01_overview
  - 06_usecases
  - 07_nfr_and_risks
  - 08_open_items
  - 09_capability_model
  - 10_data_model
  - 11_document_output_model
- required_topics:
  - 実測値と推定値の区別表示
  - 提案根拠表示
  - データ鮮度表示
  - 未決事項
- forbidden_topics:
  - 機器プロトコル詳細の露出
  - 未定義APIパラメータの断定
  - 未定義制御仕様の追加
- generation_rules:
  - must_include_open_items: true
  - must_preserve_boundary_constraints: true
  - must_not_cross_layer_responsibility: true
  - style: customer_facing
  - max_assumption_level: editorial_only

### required_sections

#### 目的
- section_id: app_sec_01
- description: 家庭内アプリの役割を要約する。
- allow_tbd: false
- forbid_inference: false
- source_requirements:
  - source_document: 01_overview
    - source_path: product_overview.purpose
    - usage_rule: summarize_only
    - required: true

#### 画面・機能要求
- section_id: app_sec_02
- description: 家庭内アプリ capability を画面・機能へ変換する。
- allow_tbd: true
- forbid_inference: false
- source_requirements:
  - source_document: 09_capability_model
    - source_path: capability_groups[target_type=user_app]
    - usage_rule: transform_to_section
    - required: true
  - source_document: 06_usecases
    - source_path: usecases[actors includes user or user_app]
    - usage_rule: transform_to_section
    - required: true

#### 表示データ仕様
- section_id: app_sec_03
- description: 表示対象の measurement / derived_metric / alert / policy を整理する。
- allow_tbd: true
- forbid_inference: true
- source_requirements:
  - source_document: 10_data_model
    - source_path: entities[category in (measurement,derived_metric,alert,policy)]
    - usage_rule: transform_to_section
    - required: true

## 21_cloud_backend_spec
- output_file: 21_cloud_backend_spec.md
- audience: mixed
- allowed_sources:
  - 01_overview
  - 04_responsibility_boundaries
  - 06_usecases
  - 07_nfr_and_risks
  - 08_open_items
  - 09_capability_model
  - 10_data_model
  - 11_document_output_model
- required_topics:
  - データ蓄積
  - 提案生成
  - 通知
  - 監査ログ
  - 未決事項
- forbidden_topics:
  - 未定義DB物理設計の断定
  - 未定義APIパラメータの断定
  - edge責務の吸収
- generation_rules:
  - must_include_open_items: true
  - must_preserve_boundary_constraints: true
  - must_not_cross_layer_responsibility: true
  - style: mixed
  - max_assumption_level: editorial_only

### required_sections

#### 責務
- section_id: cloud_sec_01
- description: クラウド責務をそのまま反映する。
- allow_tbd: false
- forbid_inference: true
- source_requirements:
  - source_document: 04_responsibility_boundaries
    - source_path: responsibility_boundaries.cloud
    - usage_rule: mandatory_extract
    - required: true

#### 機能要件
- section_id: cloud_sec_02
- description: cloud capability を機能章へ展開する。
- allow_tbd: true
- forbid_inference: false
- source_requirements:
  - source_document: 09_capability_model
    - source_path: capability_groups[target_type=cloud]
    - usage_rule: transform_to_section
    - required: true

#### データ仕様
- section_id: cloud_sec_03
- description: クラウドが扱う entity を整理する。
- allow_tbd: true
- forbid_inference: true
- source_requirements:
  - source_document: 10_data_model
    - source_path: entities
    - usage_rule: transform_to_section
    - required: true

## 22_hems_controller_spec
- output_file: 22_hems_controller_spec.md
- audience: mixed
- allowed_sources:
  - 01_overview
  - 03_vertical_slices
  - 04_responsibility_boundaries
  - 06_usecases
  - 07_nfr_and_risks
  - 08_open_items
  - 09_capability_model
  - 10_data_model
  - 11_document_output_model
- required_topics:
  - 通信方式
  - ローカル安全縮退
  - クラウド同期
  - OTA
  - 未決事項
- forbidden_topics:
  - 未定義MCU型番の断定
  - 未定義回路定数の断定
  - cloud責務の吸収
- generation_rules:
  - must_include_open_items: true
  - must_preserve_boundary_constraints: true
  - must_not_cross_layer_responsibility: true
  - style: mixed
  - max_assumption_level: editorial_only

### required_sections

#### デバイス責務
- section_id: edge_sec_01
- description: edge_controller 責務を保持する。
- allow_tbd: false
- forbid_inference: true
- source_requirements:
  - source_document: 04_responsibility_boundaries
    - source_path: responsibility_boundaries.edge_controller
    - usage_rule: mandatory_extract
    - required: true

#### Capability
- section_id: edge_sec_02
- description: HEMSコントローラ capability を展開する。
- allow_tbd: true
- forbid_inference: false
- source_requirements:
  - source_document: 09_capability_model
    - source_path: capability_groups[target_type=hems_controller]
    - usage_rule: transform_to_section
    - required: true

#### 扱うデータ
- section_id: edge_sec_03
- description: measurement/event/command/device_state/sync_status を整理する。
- allow_tbd: true
- forbid_inference: true
- source_requirements:
  - source_document: 10_data_model
    - source_path: entities[category in (measurement,event,command,device_state,sync_status)]
    - usage_rule: transform_to_section
    - required: true

## 23_firmware_spec
- output_file: 23_firmware_spec.md
- audience: engineering_facing
- allowed_sources:
  - 03_vertical_slices
  - 04_responsibility_boundaries
  - 06_usecases
  - 07_nfr_and_risks
  - 08_open_items
  - 09_capability_model
  - 10_data_model
  - 11_document_output_model
- required_topics:
  - 状態遷移
  - エラーハンドリング
  - 更新仕様
  - テスト観点
  - 未決事項
- forbidden_topics:
  - 未定義RTOS採用の断定
  - 未定義タスク周期の断定
  - 未定義メモリサイズの断定
- generation_rules:
  - must_include_open_items: true
  - must_preserve_boundary_constraints: true
  - must_not_cross_layer_responsibility: true
  - style: engineering_facing
  - max_assumption_level: light_structural

### required_sections

#### 外部要求との対応
- section_id: fw_sec_01
- description: edge capability と usecase から FW要求へ変換する。
- allow_tbd: true
- forbid_inference: false
- source_requirements:
  - source_document: 09_capability_model
    - source_path: capability_groups[target_type=hems_controller]
    - usage_rule: transform_to_section
    - required: true
  - source_document: 06_usecases
    - source_path: usecases[actors includes edge_controller]
    - usage_rule: transform_to_section
    - required: true

#### 入出力データ
- section_id: fw_sec_02
- description: edge で扱う entity を整理する。
- allow_tbd: true
- forbid_inference: true
- source_requirements:
  - source_document: 10_data_model
    - source_path: entities[category in (measurement,event,command,device_state,sync_status)]
    - usage_rule: transform_to_section
    - required: true

## 24_pcb_requirement_spec
- output_file: 24_pcb_requirement_spec.md
- audience: engineering_facing
- allowed_sources:
  - 04_responsibility_boundaries
  - 07_nfr_and_risks
  - 08_open_items
  - 09_capability_model
  - 11_document_output_model
- required_topics:
  - 通信
  - 電源
  - 更新
  - 保守
  - 安全
  - 未決事項
- forbidden_topics:
  - 未定義部品型番の断定
  - 未定義回路定数の断定
  - 未定義レイアウト仕様の断定
- generation_rules:
  - must_include_open_items: true
  - must_preserve_boundary_constraints: true
  - must_not_cross_layer_responsibility: true
  - style: engineering_facing
  - max_assumption_level: none

### required_sections

#### 上位要求の出所
- section_id: pcb_sec_01
- description: hems_controller capability と nfr から PCB要求の根拠を抽出する。
- allow_tbd: true
- forbid_inference: true
- source_requirements:
  - source_document: 09_capability_model
    - source_path: capability_groups[target_type=hems_controller]
    - usage_rule: constraint_only
    - required: true
  - source_document: 07_nfr_and_risks
    - source_path: non_functional_requirements[category in (availability,security,ota)]
    - usage_rule: constraint_only
    - required: true
