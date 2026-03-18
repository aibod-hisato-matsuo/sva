# 20. 家庭内アプリ仕様書（たたき台）

## 1. 文書情報
- project: i-Power Engine
- version: 0.1.0
- document_type: user_app_spec
- status: draft

## 2. 目的
家庭内アプリは、ユーザーが太陽光発電・蓄電池・買電/売電の状態を理解し、自らの意思で運用方針を選択し、必要に応じて提案を承認できるようにするためのフロントエンドである。

## 3. スコープ
- 現在値・履歴表示
- モード設定
- 提案表示
- 通知表示
- データ鮮度表示
- 実測/推定の区別表示

## 4. 画面・機能要求
### ダッシュボード表示
- capability_id: cap_app_001
- category: ui
- availability: required
- 説明: 現在値と履歴を表示する。
- 関連計測: m_001, m_002, m_003, m_004, m_005, m_006, m_007
- 関連コマンド: なし
- 更新周期: なし
- プロトコル: なし
- 制約:
- 実測値と推定値を区別して表示する
- 障害時挙動: なし

### モード設定
- capability_id: cap_app_002
- category: ui
- availability: required
- 説明: 見える化・提案・自動実行などのモードを設定する。
- 関連計測: なし
- 関連コマンド: なし
- 更新周期: なし
- プロトコル: なし
- 制約:
- ユーザーが意図を明示できること
- 障害時挙動: なし

### 提案承認
- capability_id: cap_app_003
- category: ui
- availability: preferred
- 説明: 提案の採用可否をユーザーが選択する。
- 関連計測: なし
- 関連コマンド: なし
- 更新周期: なし
- プロトコル: なし
- 制約:
- 提案根拠を表示すること
- 障害時挙動: なし

## 5. 対象ユースケース
### ユーザーが家庭エネルギー状態を確認する
- usecase_id: uc_001
- goal: PV・蓄電池・買電/売電の現在値と推移を理解する
- actors: user, user_app, cloud, edge_controller, smart_meter, pv_system, battery_system
- 前提条件:
- HEMS端末が機器と接続済みである
- 少なくとも1つ以上の計測チャネルが有効である
- 事後条件:
- ユーザーは実測/推定を区別して状態把握できる
- データは履歴として参照可能である

### ユーザーが節約提案を確認し設定する
- usecase_id: uc_002
- goal: 契約料金・発電状況・蓄電池状態に応じた推奨を受け取り、モードを選択する
- actors: user, user_app, cloud, external_api, battery_system
- 前提条件:
- ユーザー契約情報が登録されている
- 料金関連情報または既知の料金テーブルが利用可能である
- 事後条件:
- ユーザー方針が保存される
- 次回以降の提案・制御に反映される

## 6. 表示データ仕様
### measurement_record
- entity_id: ent_001
- category: measurement
- 説明: 計測値および推定値の共通レコード。
- 主なフィールド:
  - measurement_id (string, required=true, source=system)
  - timestamp (datetime, required=true, source=system)
  - value (number, required=true, source=measured)
  - unit (string, required=true, source=system)
  - source_type (string, required=true, source=system)
  - quality_flag (string, required=false, source=system)

### user_policy
- entity_id: ent_004
- category: policy
- 説明: ユーザーが選択した運用方針。
- 主なフィールド:
  - policy_id (string, required=true, source=system)
  - mode_name (string, required=true, source=user_input)
  - effective_from (datetime, required=false, source=system)
  - user_note (string, required=false, source=user_input)

### alert_notification
- entity_id: ent_005
- category: alert
- 説明: ユーザーまたは管理者向け通知。
- 主なフィールド:
  - alert_id (string, required=true, source=system)
  - channel (string, required=true, source=system)
  - title (string, required=true, source=derived)
  - body (string, required=true, source=derived)

### derived_metric
- entity_id: ent_009
- category: derived_metric
- 説明: 日次費用やCO2削減量などの派生指標。
- 主なフィールド:
  - metric_id (string, required=true, source=system)
  - metric_name (string, required=true, source=system)
  - value (number, required=true, source=derived)
  - calculation_basis (string, required=false, source=derived)

## 7. UI/UXルール
- 実測値と推定値は必ず明確に区別して表示する。
- 提案には必ず根拠と期待効果を表示する。
- 最新同期時刻を表示し、鮮度不足のときはユーザーへ明示する。
- 機器制御の直接プロトコルはアプリに露出しない。

## 8. 例外時表示
- 通信断時は「最新取得時刻」と「一部機能制限中」を表示する。
- 欠損値は推定値で補完する場合のみフラグ付きで表示する。
- 制御不能な提案は、提案のみ表示し、実行ボタンを出さない。

## 9. 非機能要件
### 実測/推定区分
- nfr_id: nfr_002
- category: data_quality
- requirement: 推定値は必ずフラグを持ち、UI上で実測値と明確に区別されること。
- target_value: 100%識別可能
- verification_method: UIレビューおよびAPI検証

### 提案の説明可能性
- nfr_id: nfr_004
- category: ux
- requirement: 提案表示には根拠と期待効果を併記し、ユーザーが理由を理解できること。
- target_value: 主要提案100%に根拠表示
- verification_method: UXレビュー

## 10. リスク・留意事項
### 推定値が実測値のように誤解される
- risk_id: r_002
- category: data_integrity_quality
- probability: medium
- impact: high
- priority: ★★★★☆
- mitigation: 推定フラグ、UI区別、注釈、提案根拠表示を必須化する。
- poc_validation: UXモックで認知負荷テストを行う。

### 提案が押し付けに見える
- risk_id: r_004
- category: ux_app
- probability: medium
- impact: medium
- priority: ★★★☆☆
- mitigation: 提案主体・承認主体を明確に分け、モード設定でユーザー意図を前面化する。
- poc_validation: ユーザーヒアリングとモック評価を行う。

## 11. 未決事項
- 画面一覧と画面遷移図の詳細化
- 提案カードのUI表現
- 通知チャネルの優先順位
- モバイルアプリ / Webアプリ の実装方針
