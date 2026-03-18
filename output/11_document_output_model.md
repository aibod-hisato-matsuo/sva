# 11. Document Output Model

## 家庭内アプリ仕様書
- document_id: doc_001
- audience: 顧客・開発者
- 説明: ユーザー向け画面、表示項目、提案・通知・設定を定義する。

### 目的とスコープ
- section_id: sec_app_01
- 説明: なし
- source_refs:

  - source_model: sva_design
    - path: product_overview
    - transform_rule: 要点要約
    - required: true

### 画面と機能
- section_id: sec_app_02
- 説明: なし
- source_refs:

  - source_model: capability
    - path: capability_groups[target_type=user_app]
    - transform_rule: UI capability を画面機能へ変換
    - required: true

  - source_model: usecase
    - path: usecases
    - transform_rule: ユーザー接点ありのものを抽出
    - required: true

### 表示データ
- section_id: sec_app_03
- 説明: なし
- source_refs:

  - source_model: data_model
    - path: entities[category in (measurement,derived_metric,alert)]
    - transform_rule: 表示対象データへ整理
    - required: true

## クラウド仕様書
- document_id: doc_002
- audience: 顧客・開発者
- 説明: データ蓄積、集計、提案、API、運用監視を定義する。

### 責務
- section_id: sec_cloud_01
- 説明: なし
- source_refs:

  - source_model: sva_design
    - path: responsibility_boundaries.cloud
    - transform_rule: 責務章へ展開
    - required: true

### 機能
- section_id: sec_cloud_02
- 説明: なし
- source_refs:

  - source_model: capability
    - path: capability_groups[target_type=cloud]
    - transform_rule: cloud capability を機能章へ変換
    - required: true

### データとAPI
- section_id: sec_cloud_03
- 説明: なし
- source_refs:

  - source_model: data_model
    - path: entities
    - transform_rule: 受信・保存・配信の観点で整理
    - required: true

## HEMSコントローラ仕様書
- document_id: doc_003
- audience: 顧客・開発者・組込み担当
- 説明: デバイス接続、差異吸収、安全縮退、同期を定義する。

### 責務
- section_id: sec_edge_01
- 説明: なし
- source_refs:

  - source_model: sva_design
    - path: responsibility_boundaries.edge_controller
    - transform_rule: 責務章へ展開
    - required: true

### Capability
- section_id: sec_edge_02
- 説明: なし
- source_refs:

  - source_model: capability
    - path: capability_groups[target_type=hems_controller]
    - transform_rule: device capability を列挙
    - required: true

### 扱うデータ
- section_id: sec_edge_03
- 説明: なし
- source_refs:

  - source_model: data_model
    - path: entities[category in (measurement,event,command,device_state,sync_status)]
    - transform_rule: デバイス観点へ整理
    - required: true

## ファームウェア仕様書
- document_id: doc_004
- audience: 組込み開発者
- 説明: タスク、状態遷移、取得、制御、更新を定義する。

### 外部要求との対応
- section_id: sec_fw_01
- 説明: なし
- source_refs:

  - source_model: capability
    - path: capability_groups[target_type=hems_controller]
    - transform_rule: FW要求へ展開
    - required: true

  - source_model: usecase
    - path: usecases
    - transform_rule: エッジ関与フローのみ抽出
    - required: true

## PCB要求仕様書
- document_id: doc_005
- audience: ハードウェア設計者
- 説明: 通信、電源、更新、保守用I/Fなどの要求を定義する。

### 要求の出所
- section_id: sec_pcb_01
- 説明: なし
- source_refs:

  - source_model: capability
    - path: capability_groups[target_type=hems_controller]
    - transform_rule: ハード要求に関係する capability を抽出
    - required: true

  - source_model: nfr_risk
    - path: non_functional_requirements
    - transform_rule: 安全・OTA・通信関連を抽出
    - required: true
